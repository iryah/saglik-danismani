from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
from datetime import datetime

app = Flask(__name__)

class AIHealthAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def generate_response(self, service_type, user_input):
        prompts = {
            'diagnosis': """
            Aşağıdaki semptomlar için bir ön değerlendirme yap ve hastane önerisi sun:
            Semptomlar: {user_input}
            
            Lütfen şu formatta yanıt ver:
            # ÖN DEĞERLENDİRME
            # ÖNERİLEN HASTANELER
            # ACİLİYET DURUMU
            # ÖNERİLER
            """,
            
            'psychologist': """
            Aşağıdaki durumla ilgili psikolojik değerlendirme ve öneriler sun:
            Durum: {user_input}
            
            Lütfen şu formatta yanıt ver:
            # DURUM ANALİZİ
            # ÖNERİLER
            # İLERİ DEĞERLENDİRME GEREKLİLİĞİ
            # DESTEK KAYNAKLARI
            """,
            
            'aesthetic': """
            Aşağıdaki estetik prosedür talebi için değerlendirme ve hastane önerisi sun:
            Talep: {user_input}
            
            Lütfen şu formatta yanıt ver:
            # PROSEDÜR DETAYI
            # ÖNERİLEN HASTANELER
            # TAHMİNİ MALİYET ARALIĞI
            # DİKKAT EDİLMESİ GEREKENLER
            """,
            
            'vacation': """
            Aşağıdaki kriterlere göre sağlık turizmi ve tatil önerisi sun:
            Kriterler: {user_input}
            
            Lütfen şu formatta yanıt ver:
            # ÖNERİLEN DESTINASYONLAR
            # SAĞLIK HİZMETLERİ
            # KONAKLAMA ÖNERİLERİ
            # TAHMİNİ BÜTÇE
            """,
            
            'opportunity': """
            Aşağıdaki alan için fırsat analizi yap:
            Alan: {user_input}
            
            Lütfen şu formatta yanıt ver:
            # MEVCUT FIRSATLAR
            # MALİYET ANALİZİ
            # RİSK DEĞERLENDİRMESİ
            # ÖNERİLER
            """
        }
        
        prompt = prompts[service_type].format(user_input=user_input)
        
        try:
            # Yeni API çağrısı formatı
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.7,
                system="Sen bir sağlık danışmanısın. Verilen durumu dikkatle değerlendir ve profesyonel öneriler sun.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content
        except Exception as e:
            return f"Bir hata oluştu: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/service', methods=['POST'])
def process_service():
    data = request.json
    assistant = AIHealthAssistant()
    
    service_type = data.get('service_type')
    user_input = data.get('input')
    
    if not service_type or not user_input:
        return jsonify({
            'success': False,
            'error': 'Eksik parametre'
        })
    
    response = assistant.generate_response(service_type, user_input)
    
    return jsonify({
        'success': True,
        'response': response
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
