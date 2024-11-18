from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

class SaglikAsistani:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def analiz_yap(self, service_type, durum):
        prompt = f"""
        Lütfen aşağıdaki sağlık durumu için detaylı bir değerlendirme yap:

        HİZMET TÜRÜ: {service_type}
        DURUM: {durum}

        Lütfen değerlendirmenizi şu başlıklar altında detaylandırın:

        # İLK DEĞERLENDİRME
        [Durumun detaylı analizi]

        # ÖNERİLER
        * [Öneriler listesi]

        # İLERİ ADIMLAR
        * [Yapılması gerekenler]

        # DİKKAT EDİLMESİ GEREKENLER
        * [Önemli noktalar]
        """

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                max_tokens=4000
            )
            return str(response.content)
        except Exception as e:
            return f"Bir hata oluştu: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/service', methods=['POST'])
def process_service():
    try:
        data = request.json
        asistan = SaglikAsistani()
        yanit = asistan.analiz_yap(
            data['service_type'],
            data['input']
        )
        
        return jsonify({
            'success': True,
            'response': yanit
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
