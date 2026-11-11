import os
from flask import Flask, render_template, request, jsonify
from brain_core import TheBrain
import traceback

app = Flask(__name__)

# Brain کو یہاں Initialize کریں تاکہ اگر یہاں ایرر ہو تو پتہ چل جائے
try:
    brain = TheBrain()
except Exception as e:
    print(f"Brain Initialization Error: {e}")
    brain = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if brain is None:
            return jsonify({"response": "Critical Error: Brain not initialized. Check Railway Variables."}), 500

        data = request.get_json()
        user_input = data.get("message")
        if not user_input:
            return jsonify({"response": "Please enter a message!"}), 400
        
        response = brain.process_command(user_input)
        return jsonify({"response": response})
    except Exception as e:
        # یہ اب ایرر کو براہ راست آپ کی چیٹ ونڈو میں بھیجے گا
        error_details = traceback.format_exc()
        print(error_details) 
        return jsonify({"response": f"DEBUG ERROR:\n{error_details}"}), 500

@app.route('/system_status', methods=['GET'])
def status():
    return jsonify({"status": "Online", "engine": "HuggingFace-Llama"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
