import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

class TheBrain:
    def __init__(self):
        # Now fetching the key from Railway Environment Variables
        self.api_key = os.environ.get("HF_API_KEY")
        
        if not self.api_key:
            print("CRITICAL ERROR: HF_API_KEY not found in Environment Variables!")

        self.model_id = "meta-llama/Llama-3.2-3B-Instruct" 
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.executor = ThreadPoolExecutor(max_workers=20)

    def call_llm(self, prompt):
        if not self.api_key:
            return "Error: API Key is missing. Please add HF_API_KEY in Railway Variables."

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', 'No response generated.')
                return str(result)
            elif response.status_code == 503:
                return "System is loading model, please try again in 30 seconds."
            else:
                return f"API Error: {response.status_code}"
        except Exception as e:
            return f"Connection Error: {str(e)}"

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
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_code)
            return "File updated successfully."
        except Exception as e:
            return f"Evolution failed: {str(e)}"
