import time
import random
from account_manager import AccountManager
from identity_generator import IdentityGenerator

class TikTokEngine:
    def __init__(self):
        self.acc_manager = AccountManager()
        self.id_gen = IdentityGenerator()

    def get_identity(self, account_id):
        """اکاؤنٹ کی شناخت واپس کرتا ہے (Uploader کے لیے)"""
        acc = self.acc_manager.get_all_accounts().get(account_id)
        return acc["profile"] if acc else {}

    def create_account(self, country):
        try:
            profile = self.id_gen.create_stealth_profile(country)
            username = f"user_{random.randint(100000, 999999)}_{country.lower()}"
            password = f"Pass_{random.randint(1000, 9999)}!_{country}"
            
            # انسانی طرزِ عمل کے لیے وقفہ
            time.sleep(random.uniform(3, 7))
            
            account_data = {
                "password": password,
                "country": country,
                "status": "warming",
                "profile": profile,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.acc_manager.add_account(username, account_data)
            return username
        except Exception as e:
            return None
