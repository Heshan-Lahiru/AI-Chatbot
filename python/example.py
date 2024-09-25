from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

GEMINAI_API_URL = os.getenv("GEMINAI_API_URL", "https://endpoint")  
API_KEY = os.getenv("GEMINAI_API_KEY", "your_geminai_api_key") 


logging.basicConfig(level=logging.INFO)


def get_geminai_response(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": message,
        "max_tokens": 100,
        "temperature": 0.7,  
        "top_p": 1.0,        
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    try:
        response = requests.post(GEMINAI_API_URL, json=data, headers=headers)
        response.raise_for_status() 
        return response.json().get('choices')[0].get('text').strip()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return "Sorry, I could not process your request."


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "Please send a message."}), 400

    bot_response = get_geminai_response(user_message)
    return jsonify({'response': bot_response})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify if the service is running."""
    return jsonify({'status': 'up'}), 200

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    app.run(debug=True)
