import os
import sys
from groq import Groq

# Configuration
API_KEY = "gsk_55NDVLNWHnYNfjN6VexZWGdybیہ ایرر اس لیے آ رہا ہے کیونکہ `app.py` فائل میں `brain.process_command()` کال کیا جا رہا ہے، لیکن میری پچھلی فائل میں `process_command` فنکشن کلاس کے باہر تھا، جس کی وجہ سے اسے 'TheBrain' آبجیکٹ کا حصہ نہیں سمجھا گیا۔

اسے ٹھیک کرنے کے لیے میں نے `process_command` کو کلاس کے اندر منتقل کر دیا ہے تاکہ `app.py` اسے آسانی سے ڈھونڈ سکے۔

آپ `brain_core.py` میں یہ **مکمل اور فائنل کوڈ** ڈالیں:

```python
import os
import sys
from groq import Groq

# Configuration
API\_KEY = "gsk\_55NDVLNWHnYNfjN6VexZWGdyb3FY1ZM2MpQAVa2ZldooT4WbljpK"
# Model Priority List: If the first one fails, it moves to the next
MODEL\_PRIORITY = [
    "llama-3.3-70b-versatile", 
    "llama3-70b-8192", 
    "llama-3.1-8b-instant"
]

client = Groq(api\_key=API\_KEY)

class TheBrain:
    def __init__(self):
        self.current\_model = MODEL\_PRIORITY[0]
        self.core\_files = ['app.py', 'main.py', 'brain\_core.py', 'requirements.txt']

    def get\_ai\_response(self, prompt):
        """Handles AI requests with automatic model fallback if one is decommissioned."""
        model\_index = 0
        while model\_index < len(MODEL\_PRIORITY):
            try:
                self.current\_model = MODEL\_PRIORITY[model\_index]
                chat\_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are 'The Brain', an autonomous AI engine. You must respond strictly in Roman Urdu. You can analyze code and modify files. Always provide 3 options for any task with pros and cons."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    model=self.current\_model,
                )
                return chat\_completion.choices[0].message.content
            except Exception as e:
                print(f"Model {self.current\_model} failed: {e}. Trying next model...")
                model\_index += 1
        
        return "System Error: Tamam available models fail ho chuke hain. Please API key ya model list check karein."

    def scan\_project(self):
        """Scans only core files to avoid 413 Request Entity Too Large error."""
        project\_context = ""
        for file\_name in self.core\_files:
            try:
                if os.path.exists(file\_name):
                    with open(file\_name, 'r', encoding='utf-8') as f:
                        project\_context += f"\n--- File: {file\_name} ---\n{f.read()}\n"
            except Exception as e:
                project\_context += f"\nError reading {file\_name}: {e}\n"
        return project\_context

    def rewrite\_file(self, file\_name, content):
        """Writes or modifies the specified file."""
        try:
            with open(file\_name, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully updated {file\_name}."
        except Exception as e:
            return f"Error updating {file\_name}: {e}"

    def restart\_server(self):
        """Restarts the Flask server to apply changes."""
        try:
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            return f"Restart failed: {e}"

    def process\_command(self, user\_input):
        """Main entry point for app.py to communicate with the AI."""
        # 1. Scan the project for context
        context = self.scan\_project()
        
        # 2. Construct the prompt for the AI
        full\_prompt = f"Project Context:\n{context}\n\nUser Command: {user\_input}\n\nRespond in Roman Urdu."
        
        # 3. Get response from AI (with fallback)
        response = self.get\_ai\_response(full\_prompt)
        
        return response

# Initialize The Brain object
brain = TheBrain()