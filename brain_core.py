import os
from groq import Groq

API_KEY = "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"
client = Groq(api_key=API_KEY)

class TheBrain:
    def __init__(self):
        self.project_root = os.getcwd()
        self.identity = "The Brain - Lead Architect"

    def scan_all_files(self):
        files_data = {}
        # صرف ضروری فائلیں سکین کریں تاکہ 'Request Too Large' ایرر نہ آئے
        for file in ['app.py', 'main.py', 'brain_core.py']:
            path = os.path.join(self.project_root, file)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    files_data[path] = f.read()
        return files_data

    def rewrite_file(self, path, content):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e: return str(e)

    def process_command(self, user_input):
        context = self.scan_all_files()
        # یہاں میں نے اسے سخت ہدایت دی ہے کہ جواب رومن اردو میں دے
        system_prompt = f"""
        Identity: {self.identity}. 
        You are a Master AI Agent. 
        IMPORTANT: Always respond in Roman Urdu (like 'Main aapka system handle kar raha hoon').
        Context: {context}
        
        If the user wants a code change, provide:
        ACTION: UPDATE_FILE | FILE: [path] | CONTENT: [code] | MESSAGE: [Roman Urdu explanation]
        Otherwise:
        ACTION: RESPONSE | MESSAGE: [Roman Urdu answer]
        """
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
        )
        return completion.choices[0].message.content

brain = TheBrain()