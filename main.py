import os
from flask import Flask, render_template, request, jsonify
from brain_core import BrainCore

app = Flask(__name__)
brain = BrainCore()

# Safe-Execution Wrapper: تاکہ اگر برین میں کوئی مسئلہ ہو تو ویب سائٹ بلیک سکرین نہ ہو
@app.route('/')
def index():
    return render_template('brain_chat.html')

@app.route('/brain/command', methods=['POST'])
def handle_command():
    try:
        data = request.json
        user_input = data.get("message", "")
        auth_key = request.headers.get("X-Master-Key")

        # Master Key Security Check
        if not brain.verify_key(auth_key):
            return jsonify({"response": "❌ غیر مجاز رسائی! ماسٹر کی (Master Key) غلط ہے۔", "status": "error"}), 403

        # Brain processes the command
        response = brain.execute_command(user_input)
        return jsonify({"response": response, "status": "success"})
    except Exception as e:
        return jsonify({"response": f"⚠️ سسٹم ایرر: {str(e)}۔ منشی اسے ٹھیک کرنے کی کوشش کر رہا ہے...", "status": "error"}), 500

if __name__ == '__main__':
    # Railway deployment ready
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
