import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

class TheBrain:
    def __init__(self):
        self.api_key = os.environ.get("HF_API_KEY")
        
        # Priority List of Models: If one fails, the system automatically shifts to the next
        self.model_priority_list = [
            "meta-llama/Llama-3.2-3B-Instruct",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "google/gemma-2-9b-it"
        ]
        self.current_model_index = 0
        self.executor = ThreadPoolExecutor(max_workers=20)

    def get_current_model(self):
        return self.model_priority_list[self.current_model_index]

    def call_llm(self, prompt):
        if not self.api_key:
            return "Critical Error: API Key missing in Railway Variables."

        # Try models until one works or all fail
        attempts = 0
        max_attempts = len(self.model_priority_list)

        while attempts < max_attempts:
            model_id = self.get_current_model()
            api_url = f"https://api-inference.huggingface.co/models/{model_id}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 500, "temperature": 0.7, "return_full_text": False}
            }

            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get('generated_text', 'No response generated.')
                    return str(result)
                
                elif response.status_code == 503:
                    # Model is loading, wait a bit and try again or shift
                    time.sleep(2)
                    attempts += 1
                    self.shift_model()
                else:
                    attempts += 1
                    self.shift_model()

            except Exception as e:
                attempts += 1
                self.shift_model()
                print(f"Model {model_id} failed: {e}")

        return "All available AI models failed to respond. Please check network or API limits."

    def shift_model(self):
        # Shift to the next model in the priority list
        self.current_model_index = (self.current_model_index + 1) % len(self.model_priority_list)
        print(f"Self-Evolving: Shifting to model {self.get_current_model()}")

    def process_command(self, user_input):
        system_prompt = (
            "You are 'The Brain', a stealthy TikTok management engine. "
            "Strict Rules: 1. Always respond in Roman Urdu. "
            "2. For every problem, provide 3 distinct options with Pros and Cons. "
            "3. Be concise and technical. "
            "User says: "
        )
        full_prompt = f"{system_prompt} {user_input}"
        time.sleep(1) 
        return self.call_llm(full_prompt)

    def self_evolve(self, file_path, new_code):
        # Capability to rewrite and repair its own logic
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_code)
            return "Self-Repair successful: File updated."
        except Exception as e:
            return f"Self-Repair failed: {str(e)}"
