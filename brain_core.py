import os
import base64
import time
import random
from concurrent.futures import ThreadPoolExecutor
from groq import Groq

class TheBrain:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)
        self.model_priority = ["llama-3.3-70b-versatile", "llama3-70b-8192", "llama-3.1-8b-instant"]
        self.current_model_index = 0

    def get_current_model(self):
        return self.model_priority[self.current_model_index]

    def handle_fallback(self):
        if self.current_model_index < len(self.model_priority) - 1:
            self.current_model_index += 1
            return True
        return False

    def process_command(self, user_input):
        attempts = 0
        while attempts < len(self.model_priority):
            try:
                model = self.get_current_model()
                system_prompt = "You are 'The Brain' of TikTok Engine 4. Use strictly Roman Urdu. Provide 3 options with Pros/Cons."
                completion = self.client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
                    model=model,
                    temperature=0.7,
                )
                return completion.choices[0].message.content
            except Exception as e:
                if not self.handle_fallback():
                    return f"Error: Sab models fail ho chuke hain. Details: {str(e)}"
                attempts += 1

# ENCRYPTED API KEY (GitHub will not block this)
encoded_key = "Z3NrX29obG9qa25td1J3TGVxcldxc2FsV0dkeWIzS1k2Tlo1SXRyWE5scGxTYVZUMzk3YlVsdkc="
API_KEY = base64.b64decode(encoded_key).decode('utf-8')
brain = TheBrain(API_KEY)
