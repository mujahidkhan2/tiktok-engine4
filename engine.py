import time
import random
from account_manager import AccountManager
from identity_generator import IdentityGenerator

class TikTokEngine:
    def __init__(self):
        self.acc_manager = AccountManager()
        self.id_gen = IdentityGenerator()

    def create_single_account(self, country):
        # ایک اکاؤنٹ بنانے کی لاجک (اسٹیلتھ موڈ)
        try:
            # 1. شناخت بنانا
            profile = self.id_gen.create_stealth_profile(country)
            username = f"user_{random.randint(100000, 999999)}_{country.lower()}"
            password = f"Pass_{random.randint(1000, 9999)}!_{country}"
            
            # 2. یہاں اصل API کال یا آٹومیشن آئے گی (Simulated for now)
            time.sleep(random.uniform(2, 5)) # ہیومن تاخیر تاکہ سرور کریش نہ ہو
            
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
            print(f"Error creating account for {country}: {e}")
            return None

    def create_batch_accounts(self, total_count, custom_specs=None):
        # بوجھ کو تقسیم کرنے کے لیے بیچ پروسیسنگ
        created_count = 0
        
        if custom_specs:
            for country, count in custom_specs.items():
                for _ in range(count):
                    if self.create_single_account(country):
                        created_count += 1
                    time.sleep(random.uniform(1, 3)) # سرور پر بوجھ کم کرنے کے لیے وقفہ
        else:
            for _ in range(total_count):
                if self.create_single_account("USA"): # Default
                    created_count += 1
                time.sleep(random.uniform(1, 3))
        
        return created_count

    def get_system_status(self):
        accs = self.acc_manager.get_all_accounts()
        return {
            "system_health": "Healthy" if len(accs) < 5000 else "Heavy Load",
            "total_accounts": len(accs)
        }
