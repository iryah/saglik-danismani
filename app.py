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
        prompts = {
            'diagnosis': f"""
                Bir sağlık uzmanı olarak aşağıdaki semptomlara göre değerlendirme yap:
                DURUM: {durum}

                # SEMPTOM ANALİZİ
                [Belirtilerin detaylı analizi]

                # ÖN DEĞERLENDİRME
                [Olası durumlar]

                # ÖNERİLER
                * Yapılması gerekenler
                * İlaç önerileri (varsa)
                * Yaşam tarzı önerileri

                # ACİLİYET DURUMU
                [Durumun aciliyeti ve hastaneye gitme gerekliliği]

                # UZMAN YÖNLENDİRMESİ
                [Hangi uzmana gidilmeli]
            """,
            
            'psychologist': f"""
                Bir psikolojik danışman olarak aşağıdaki durumu değerlendir:
                DURUM: {durum}

                # DURUM ANALİZİ
                [Psikolojik durumun analizi]

                # BAŞA ÇIKMA STRATEJİLERİ
                * Önerilen teknikler
                * Günlük uygulamalar
                * Yaşam tarzı değişiklikleri

                # PROFESYONEL DESTEK GEREKLİLİĞİ
                [Uzman desteği gerekli mi?]

                # İLERİ ADIMLAR
                [Atılması gereken adımlar]
            """,
            
            'aesthetic': f"""
                Bir estetik danışmanı olarak aşağıdaki talebi değerlendir:
                DURUM: {durum}

                # PROSEDÜR BİLGİSİ
                [İstenilen işlemin detayları]

                # UYGUNLUK DEĞERLENDİRMESİ
                [İşlemin uygunluğu ve riskleri]

                # HASTANE ÖNERİLERİ
                * Önerilen merkezler
                * Uzman önerileri

                # MALİYET TAHMİNİ
                [Yaklaşık maliyet aralığı]

                # DİKKAT EDİLECEKLER
                [İşlem öncesi ve sonrası]
            """,
            
            'vacation': f"""
                Bir sağlık turizmi danışmanı olarak öneride bulun:
                DURUM: {durum}

                # DESTİNASYON ÖNERİLERİ
                * Önerilen şehirler/ülkeler
                * Sağlık merkezleri

                # KONAKLAMA
                * Hastane yakını oteller
                * Özel bakım tesisleri

                # ULAŞIM
                [Ulaşım önerileri ve dikkat edilecekler]

                # MALİYET PLANLAMASI
                * Tedavi maliyetleri
                * Konaklama maliyetleri
                * Ek masraflar
            """,
            
            'opportunity': f"""
                Bir sağlık sektörü analisti olarak fırsat analizi yap:
                ALAN: {durum}

                # PAZAR ANALİZİ
                [Mevcut durum ve trendler]

                # FIRSATLAR
                * Kısa vadeli fırsatlar
                * Uzun vadeli fırsatlar

                # RİSK ANALİZİ
                [Olası riskler ve önlemler]

                # YATIRIM GEREKSİNİMLERİ
                [Gerekli kaynaklar ve maliyetler]
            """
        }

        try:
            selected_prompt = prompts.get(service_type, prompts['diagnosis'])
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{
                    "role": "user", 
                    "content": selected_prompt
                }],
                max_tokens=4000
            )
            return {
                'success': True,
                'response': str(response.content)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/service', methods=['POST'])
def process_service():
    try:
        data = request.json
        if not data or 'service_type' not in data or 'input' not in data:
            return jsonify({
                'success': False,
                'error': 'Eksik veri gönderildi'
            }), 400
            
        asistan = SaglikAsistani()
        result = asistan.analiz_yap(
            data['service_type'],
            data['input']
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Hata yakalama
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'Sayfa bulunamadı'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Sunucu hatası'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
