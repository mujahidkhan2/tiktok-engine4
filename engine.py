import time
import random
from account_manager import AccountManager
from identity_generator import IdentityGenerator

class TikTokEngine:
    def __init__(self):
        self.acc_manager = AccountManager()
        self.id_gen = IdentityGenerator()

    def get_identity(self, account_id):
        acc = self.acc_manager.get_all_accounts().get(account_id)
        return acc["profile"] if acc else {}

    def create_account(self, country):
        try:
            profile = self.id_gen.create_stealth_profile(country)
            username = f"user_{random.randint(100000, 999999)}_{country.lower()}"
            password = f"Pass_{random.randint(1000, 9999)}!_{country}"
            
            time.sleep(random.uniform(5, 15))
            
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
        """
        This is where the 'Muzdoor' performs the specific human-like task
        """
        try:
            print(f"Account {acc_id} starting action {action_type} on {target_url}")
            
            if action_type == 'full_support':
                # Simulation: Watch 100% -> Like -> Comment -> Follow
                time.sleep(random.randint(30, 60)) # Watch time
                print(f"✅ {acc_id} fully watched and liked.")
            
            elif action_type == 'casual_like':
                # Simulation: Watch 30% -> Like
                time.sleep(random.randint(10, 20)) 
                print(f"✅ {acc_id} gave a quick like.")
                
            elif action_type == 'ghost_view':
                # Simulation: Just watch and leave
                time.sleep(random.randint(20, 40))
                print(f"✅ {acc_id} viewed the content.")
                
            return True
        except Exception as e:
            print(f"Boost Error for {acc_id}: {e}")
            return False

    def replace_banned_account(self, banned_id, country, health_tracker):
        reason = health_tracker.analyze_rejection(banned_id)
        self.acc_manager.remove_account(banned_id) 
        print(f"Replacing {banned_id} due to {reason}...")
        return self.create_account(country)