import os
import sys
import subprocess
from groq import Groq

# Configuration
API_KEY = "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"
# Model Priority List: If the first one fails, it moves to the next
MODEL_PRIORITY = [
    "llama-3.3-70b-versatile", 
    "llama3-70b-8192", 
    "llama-3.1-8b-instant"
]

client = Groq(api_key=API_KEY)

class TheBrain:
    def __init__(self):
        self.current_model = MODEL_PRIORITY[0]
        self.core_files = ['app.py', 'main.py', 'brain_core.py', 'requirements.txt']

    def get_ai_response(self, prompt):
        """Handles AI requests with automatic model fallback if one is decommissioned."""
        model_index = 0
        while model_index < len(MODEL_PRIORITY):
            try:
                self.current_model = MODEL_PRIORITY[model_index]
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are 'The Brain', an autonomous AI engine. You must respond strictly in Roman Urdu. You can analyze code and modify files. Always provide 3 options for any task with pros and cons."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    model=self.current_model,
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                print(f"Model {self.current_model} failed: {e}. Trying next model...")
                model_index += 1
        
        return "System Error: Tamam available models fail ho chuke hain. Please API key ya model list check karein."

    def scan_project(self):
        """Scans only core files to avoid 413 Request Entity Too Large error."""
        project_context = ""
        for file_name in self.core_files:
            try:
                if os.path.exists(file_name):
                    with open(file_name, 'r', encoding='utf-8') as f:
                        project_context += f"\n--- File: {file_name} ---\n{f.read()}\n"
            except Exception as e:
                project_context += f"\nError reading {file_name}: {e}\n"
        return project_context

    def rewrite_file(self, file_name, content):
        """Writes or modifies the specified file."""
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully updated {file_name}."
        except Exception as e:
            return f"Error updating {file_name}: {e}"

    def restart_server(self):
        """Restarts the Flask server to apply changes."""
        try:
            # This assumes the app is run via a process manager like Gunicorn on Railway
            # In a real Docker/Railway env, a file change often triggers auto-restart.
            # This is a fallback to force process termination.
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            return f"Restart failed: {e}"

# Initialize The Brain
brain = TheBrain()

def process_command(user_input):
    # 1. Scan the project for context
    context = brain.scan_project()
    
    # 2. Construct the prompt for the AI
    full_prompt = f"Project Context:\n{context}\n\nUser Command: {user_input}\n\nRespond in Roman Urdu."
    
    # 3. Get response from AI (with fallback)
    response = brain.get_ai_response(full_prompt)
    
    return response