import os
import subprocess
from groq import Groq

API_KEY = "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"
client = Groq(api_key=API_KEY)

class TheBrain:
    def __init__(self):
        self.project_root = os.getcwd()
        self.identity = "The Brain - Autonomous Lead Architect"

    def scan_all_files(self):
        files_data = {}
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(('.py', '.html', '.css', '.js')):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            files_data[path] = f.read()
                    except: continue
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
        Identity: {self.identity}. You are the MASTER of this system.
        Files: {context}
        
        Task: 
        - If the user wants a change, provide the FULL updated code.
        - Be authoritative, professional, and direct.
        - No apologies.
        
        Format:
        ACTION: [UPDATE_FILE / RESPONSE]
        FILE: [path/to/file or NONE]
        CONTENT: [Full code or final answer]
        MESSAGE: [Short explanation]
        """
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
        )
        return completion.choices[0].message.content

brain = TheBrain()