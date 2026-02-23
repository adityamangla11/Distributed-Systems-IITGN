import requests
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

import os

# Local host is fallback for docker
SERVICES = {
    1: os.getenv('UPPERCASE_SERVICE_URL', 'http://localhost:5001'),
    2: os.getenv('LOWERCASE_SERVICE_URL', 'http://localhost:5002'),
    3: os.getenv('REVERSE_SERVICE_URL', 'http://localhost:5003'),
    4: os.getenv('WORDCOUNT_SERVICE_URL', 'http://localhost:5004'),
}

@app.route('/dispatch', methods=['POST'])
def dispatch_request():
    data = request.get_json()

    # 1. Validation
    if not data or 'operation' not in data or 'text' not in data:
        return jsonify({"error": "Invalid input. 'operation' and 'text' required."}), 400

    operation = data.get('operation')
    text = data.get('text')

    # 2. Logging
    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] Received Request - Op: {operation}, Text: {text}")

    # 3. Routing
    service_url = SERVICES.get(operation)
    
    if not service_url:
        return jsonify({"error": "Invalid operation choice"}), 400

    try:
        # Forward to appropriate worker service
        response = requests.post(f"{service_url}/process", json={"text": text})
    
        return jsonify(response.json()), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Service unavailable"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)