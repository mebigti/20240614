from flask import Flask, request, jsonify, send_from_directory
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('userInput', '')

    curl_command = [
        'curl', 'http://localhost:8080/v1/chat/completions',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Bearer no-key',
        '-d', json.dumps({
            'model': 'LLaMA_CPP',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are LLAMAfile, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests.'
                },
                {
                    'role': 'user',
                    'content': user_input
                }
            ]
        })
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)
    response = result.stdout

    try:
        json_response = json.loads(response)
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to decode response from server'}), 500

    return jsonify(json_response)

if __name__ == '__main__':
    app.run(port=5000)
