from flask import Flask, render_template, request, jsonify
from brain_core import brain
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('brain_chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("message")
        if not user_input:
            return jsonify({"status": "error", "message": "No message provided"}), 400

        response_text = brain.process_command(user_input)
        
        lines = response_text.split('\n')
        action, file_path, content, message = "", "", "", ""
        
        for line in lines:
            if line.startswith("ACTION:"): action = line.replace("ACTION:", "").strip()
            if line.startswith("FILE:"): file_path = line.replace("FILE:", "").strip()
            if line.startswith("MESSAGE:"): message = line.replace("MESSAGE:", "").strip()

        if action == "UPDATE_FILE" and file_path:
            full_content = response_text.split("CONTENT:")[1].split("MESSAGE:")[0].strip()
            brain.rewrite_file(file_path, full_content)
            return jsonify({"status": "updated", "message": message if message else "System updated successfully."})
        
        # If it's just a response, return the content part or the whole thing
        final_msg = response_text.split("MESSAGE:")[1].strip() if "MESSAGE:" in response_text else response_text
        return jsonify({"status": "response", "message": final_msg})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": f"System Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Railway uses port 8080 or provided PORT env variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)