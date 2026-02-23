from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. JSON with 'text' field required."}), 400
    
    input_text = data['text']

    if not input_text.strip():
        return jsonify({"error": "Input text cannot be empty"}), 400

    word_count = len(input_text.split())

    return jsonify({"result": word_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)