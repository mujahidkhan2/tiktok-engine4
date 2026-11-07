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
            # Use Identity Generator to create a unique profile based on country
            profile = self.id_gen.create_stealth_profile(country)
            username = f"user_{random.randint(100000, 999999)}_{country.lower()}"
            password = f"Pass_{random.randint(1000, 9999)}!_{country}"
            
            # Human-like delay during creation
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

    def replace_banned_account(self, banned_id, country, health_tracker):
        """Replaces a banned account with a new one that avoids previous mistakes"""
        reason = health_tracker.analyze_rejection(banned_id)
        self.acc_manager.remove_account(banned_id) # Wipe data completely
        
        # Create new account with adjusted parameters based on ban reason
        print(f"Replacing {banned_id} due to {reason}...")
        return self.create_account(country)