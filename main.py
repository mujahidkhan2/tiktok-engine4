import os
from flask import Flask, render_template, request, jsonify
from brain_core import TheBrain
import traceback

app = Flask(__name__)
brain = TheBrain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")
        if not user_input:
            return jsonify({"response": "Please enter a message!"}), 400
        
        response = brain.process_command(user_input)
        return jsonify({"response": response})
    except Exception as e:
        # یہ حصہRailway کے لاگز میں بتائے گا کہ اصل مسئلہ کیا ہے
        print("--- SYSTEM ERROR ---")
        traceback.print_exc() 
        return jsonify({"response": f"Server Error: {str(e)}"}), 500

@app.route('/system_status', methods=['GET'])
def status():
    return jsonify({"status": "Online", "engine": "HuggingFace-Llama"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
