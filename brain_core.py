import os
import time
import random
from concurrent.futures import ThreadPoolExecutor
from groq import Groq

class TheBrain:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)
        
        # Model Priority List for Dynamic Fallback to prevent 400/404 errors
        self.model_priority = [
            "llama-3.3-70b-versatile", 
            "llama3-70b-8192", 
            "llama-3.1-8b-instant"
        ]
        self.current_model_index = 0

    def get_current_model(self):
        return self.model_priority[self.current_model_index]

    def handle_fallback(self):
        """Shift to the next model in the priority list if the current one fails."""
        if self.current_model_index < len(self.model_priority) - 1:
            self.current_model_index += 1
            print(f"Switching to fallback model: {self.get_current_model()}")
            return True
        return False

    def process_command(self, user_input):
        """Main intelligence module to handle commands in Roman Urdu."""
        attempts = 0
        max_attempts = len(self.model_priority)

        while attempts < max_attempts:
            try:
                model = self.get_current_model()
                
                # System prompt to enforce Roman Urdu and Intelligence requirements
                system_prompt = (
                    "You are 'The Brain', the intelligence module of a Stealthy TikTok Management Engine. "
                    "Your language MUST be strictly Roman Urdu. "
                    "For every task, provide 3 different options with their Pros and Cons. "
                    "You have the capability to analyze and rewrite your own core files (app.py, brain_core.py). "
                    "Keep your tone professional, stealthy, and highly technical."
                )

                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input},
                    ],
                    model=model,
                    temperature=0.7,
                )
                
                return chat_completion.choices[0].message.content

            except Exception as e:
                print(f"Error with model {self.get_current_model()}: {str(e)}")
                if not self.handle_fallback():
                    return "Sorry, tamam available models fail ho chuke hain. Please API key check karein."
                attempts += 1

    def execute_stealth_task(self, tasks):
        """Parallel execution with randomized sleep for stealth."""
        def worker(task):
            # Randomized sleep to avoid detection
            time.sleep(random.uniform(1, 5))
            print(f"Executing task: {task}")
            return f"Task {task} completed stealthily."

        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(worker, tasks))
        return results

# API KEY is now fetched from Railway Environment Variables for security and stability
API_KEY = os.getenv("GROQ_API_KEY")
brain = TheBrain(API_KEY)