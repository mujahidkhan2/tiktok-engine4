from flask import Flask, request, jsonify, render_template_string
from brain_core import brain

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>THE BRAIN | Intelligence Center</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        #header { background: #fff; padding: 20px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-weight: bold; font-size: 20px; }
        #chat-box { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 10px 15px; border-radius: 15px; max-width: 80%; word-wrap: break-word; }
        .user { align-self: flex-end; background: #007bff; color: white; }
        .bot { align-self: flex-start; background: white; color: #333; border: 1px solid #ddd; }
        #input-area { background: #fff; padding: 20px; display: flex; gap: 10px; border-top: 1px solid #ddd; }
        input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; outline: none; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div id="header">THE BRAIN | Intelligence Center</div>
    <div id="chat-box" id="chatBox"></div>
    <div id="input-area">
        <input type="text" id="userInput" placeholder="Type a command...">
        <button onclick="sendMsg()">Send</button>
    </div>
    <script>
        async function sendMsg() {
            const input = document.getElementById('userInput');
            const box = document.getElementById('chat-box');
            if(!input.value) return;
            box.innerHTML += `<div class="msg user">${input.value}</div>`;
            const val = input.value; input.value = '';
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: val})
            });
            const data = await res.json();
            box.innerHTML += `<div class="msg bot">${data.response}</div>`;
            box.scrollTop = box.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')
    response = brain.process_command(prompt)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
