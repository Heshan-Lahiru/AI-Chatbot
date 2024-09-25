from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

GEMINAI_API_KEY = os.getenv('GEMINAI_API_KEY')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        # API request setup
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINAI_API_KEY}'
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": user_input}]}]
        }

        # API request
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            return jsonify({'error': 'Failed to connect to AI', 'details': response.text}), 500

        # Parse AI response
        ai_reply = response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response from AI')

        return jsonify({'reply': ai_reply})

    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
