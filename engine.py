import time
import random
from account_manager import AccountManager
from identity_generator import IdentityGenerator

class TikTokEngine:
    def __init__(self):
        self.acc_manager = AccountManager()
        self.id_gen = IdentityGenerator()

    def create_account(self, country):
        try:
            profile = self.id_gen.create_stealth_profile(country)
            username = f"user_{random.randint(100000, 999999)}_{country.lower()}"
            password = f"Pass_{random.randint(1000, 9999)}!_{country}"
            
            time.sleep(random.uniform(2, 10)) 
            
            account_data = {
                "password": password,
                "country": country,
                "status": "warming",
                "profile": profile,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "trust_score": random.uniform(40, 70)
            }
            
            self.acc_manager.add_account(username, account_data)
            return username
        except Exception as e:
            print(f"Creation Error: {e}")
            return None

    def execute_boost_action(self, acc_id, target_url, action_type):
        try:
            # Human Mimicry: Random delays to prevent bans
            if action_type == 'full_support':
                time.sleep(random.randint(40, 80)) 
            elif action_type == 'casual_like':
                time.sleep(random.randint(15, 30))
            elif action_type == 'ghost_view':
                time.sleep(random.randint(25, 50))
            return True
        except Exception as e:
            print(f"Boost Error: {e}")
            return False