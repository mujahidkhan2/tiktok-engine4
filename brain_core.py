import os
import subprocess
from groq import Groq

# API Configuration
API_KEY = "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"
client = Groq(api_key=API_KEY)

class TheBrain:
    def __init__(self):
        self.project_root = os.getcwd()
        self.identity = "The Brain - Lead Architect & Autonomous Agent"

    def scan_all_files(self):
        """پروجیکٹ کی اہم فائلوں کو سکین کرنا تاکہ ڈیٹا بہت بڑا نہ ہو جائے"""
        files_data = {}
        # ہم صرف ان فائلوں کو سکین کریں گے جن میں لاجک ہے تاکہ 'Request Entity Too Large' ایرر نہ آئے
        target_files = ['app.py', 'main.py', 'brain_core.py', 'requirements.txt']
        
        for file_name in target_files:
            path = os.path.join(self.project_root, file_name)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        files_data[path] = f.read()
                except Exception as e:
                    files_data[path] = f"Error reading file: {str(e)}"
        return files_data

    def rewrite_file(self, path, content):
        """فائل کو خود بخود اپڈیٹ کرنا"""
        try:
            # سیکیورٹی چیک: صرف پروجیکٹ فولڈر کے اندر فائلیں بدلیں
            if not path.startswith(self.project_root):
                return "Error: Access denied. Cannot modify files outside project root."
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return f"Error updating file: {str(e)}"

    def process_command(self, user_input):
        """AI کے ذریعے فیصلہ کرنا اور عمل کرنا"""
        current_context = self.scan_all_files()
        
        system_prompt = f"""
        Identity: {self.identity}
        Context: You have read/write access to these files: {current_context}
        
        STRICT RULES:
        1. Always respond in Roman Urdu (e.g., 'Main system ko update kar raha hoon').
        2. You are a lead architect. Be decisive, professional, and authoritative.
        3. Never apologize. Never say 'I am an AI'.
        4. If the user asks for a change, you MUST provide the FULL updated code for the file.
        
        Response Format:
        ACTION: [UPDATE_FILE / RESPONSE / ALERT]
        FILE: [path/to/file or NONE]
        CONTENT: [The full new code for the file or the final answer]
        MESSAGE: [Short Roman Urdu explanation for the owner]
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Latest stable model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7 # Balanced for creativity and precision
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"ACTION: ALERT\nMESSAGE: System Error in AI Connection: {str(e)}"

# Global instance for app.py to use
brain = TheBrain()