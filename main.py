import os
from flask import Flask, render_template, request, jsonify
from brain_core import TheBrain

app = Flask(__name__)
brain = TheBrain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = brain.process_command(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

@app.route('/system_status', methods=['GET'])
def status():
    return jsonify({"status": "Online", "engine": "HuggingFace-Llama"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))