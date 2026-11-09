from flask import Flask, render_template, request, jsonify
from brain_core import brain

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('brain_chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message")
    response_text = brain.process_command(user_input)
    
    # Parsing the Brain's decision
    lines = response_text.split('\n')
    action = ""
    file_path = ""
    content = ""
    message = ""
    
    for line in lines:
        if line.startswith("ACTION:"): action = line.replace("ACTION:", "").strip()
        if line.startswith("FILE:"): file_path = line.replace("FILE:", "").strip()
        if line.startswith("CONTENT:"): content = line.replace("CONTENT:", "").strip()
        if line.startswith("MESSAGE:"): message = line.replace("MESSAGE:", "").strip()

    if action == "UPDATE_FILE" and file_path and content:
        # Extracting full content if it's multi-line
        full_content = response_text.split("CONTENT:")[1].split("MESSAGE:")[0].strip()
        brain.rewrite_file(file_path, full_content)
        return jsonify({"status": "updated", "message": message})
    
    return jsonify({"status": "response", "message": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
