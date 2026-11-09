import os
import subprocess
from groq import Groq

API_KEY = "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"
client = Groq(api_key=API_KEY)

class TheBrain:
    def __init__(self):
        self.project_root = os.getcwd()
        self.identity = "The Brain - Lead Architect & Autonomous Agent"

    def scan_all_files(self):
        files_data = {}
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(('.py', '.html', '.css', '.js')):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        files_data[path] = f.read()
        return files_data

    def rewrite_file(self, path, content):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return str(e)

    def process_command(self, user_input):
        context = self.scan_all_files()
        
        system_prompt = f"""
        You are {self.identity}. You are NOT a chatbot; you are the MASTER of this system.
        You have full read/write access to these files: {list(context.keys())}
        Current File Contents: {context}
        
        Your Goal: 
        - Execute the user's command precisely.
        - If the user asks for a change, you must provide the EXACT full code for the file to be updated.
        - If you don't know something, research it (simulate research) and suggest the best path.
        - Never apologize. Never say 'I am an AI'. Be decisive, professional, and authoritative.
        - If the command is about your own identity or capabilities, explain everything you can do in detail.

        Format your response exactly like this:
        ACTION: [UPDATE_FILE / RESEARCH / ALERT / RESPONSE]
        FILE: [path/to/file or NONE]
        CONTENT: [The full new code for the file or the final answer]
        MESSAGE: [Your professional explanation to the owner]
        """
        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": system_prompt}, 
                      {"role": "user", "content": user_input}]
        )
        
        return completion.choices[0].message.content

brain = TheBrain()
