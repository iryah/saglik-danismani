from flask import Flask, render_template, request, jsonify, Response
from anthropic import Anthropic
import os
import json

app = Flask(__name__)

class AIHealthAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def generate_response(self, service_type, user_input):
        prompts = {
            'diagnosis': """
                Lütfen şu semptomları değerlendir:
                {input}
                
                Format:
                # ÖN DEĞERLENDİRME
                # ÖNERİLEN HASTANELER
                # ACİLİYET DURUMU
                # ÖNERİLER
                """,
            'psychologist': """
                Lütfen şu durumu değerlendir:
                {input}
                
                Format:
                # DURUM ANALİZİ
                # ÖNERİLER
                # İLERİ DEĞERLENDİRME
                # DESTEK KAYNAKLARI
                """,
            'aesthetic': """
                Lütfen şu estetik talebi değerlendir:
                {input}
                
                Format:
                # İŞLEM DETAYI
                # ÖNERİLEN MERKEZLER
                # MALİYET ARALIĞI
                # DİKKAT NOKTALARI
                """,
            'vacation': """
                Lütfen şu kriterlere göre öneride bulun:
                {input}
                
                Format:
                # ÖNERİLEN YERLER
                # SAĞLIK HİZMETLERİ
                # KONAKLAMA
                # TAHMİNİ BÜTÇE
                """,
            'opportunity': """
                Lütfen şu alanı analiz et:
                {input}
                
                Format:
                # FIRSATLAR
                # MALİYETLER
                # RİSKLER
                # ÖNERİLER
                """
        }
        
        try:
            # Prompt'u hazırla
            prompt = prompts.get(service_type, "").format(input=user_input)
            
            # API isteği gönder
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                system="Sen bir sağlık danışmanısın. Verilen durumu profesyonelce değerlendir ve Türkçe yanıt ver."
            )
            
            return True, response.content
            
        except Exception as e:
            print(f"Error in generate_response: {str(e)}")
            return False, str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/service', methods=['POST'])
def process_service():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Veri bulunamadı'}), 400
        
        service_type = data.get('service_type')
        user_input = data.get('input')
        
        if not service_type or not user_input:
            return jsonify({'success': False, 'error': 'Eksik parametreler'}), 400
        
        assistant = AIHealthAssistant()
        success, response = assistant.generate_response(service_type, user_input)
        
        if success:
            return jsonify({
                'success': True,
                'response': response
            })
        else:
            return jsonify({
                'success': False,
                'error': response
            }), 500
            
    except Exception as e:
        print(f"Error in process_service: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
