from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

class AIHealthAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def generate_response(self, service_type, user_input):
        try:
            prompt = f"Sağlık danışmanı olarak şu konuda yardım et: {service_type}\nDurum: {user_input}"
            
            # Doğru API kullanımı
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return True, response.content
        except Exception as e:
            return False, str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/service', methods=['POST'])
def process_service():
    try:
        data = request.get_json()
        service_type = data.get('service_type')
        user_input = data.get('input')
        
        if not service_type or not user_input:
            return jsonify({'success': False, 'error': 'Eksik parametre'})
        
        assistant = AIHealthAssistant()
        success, response = assistant.generate_response(service_type, user_input)
        
        if success:
            return jsonify({'success': True, 'response': response})
        else:
            return jsonify({'success': False, 'error': response})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
