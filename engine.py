import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from account_manager import AccountManager

class TikTokEngine:
    def __init__(self):
        self.acc_manager = AccountManager()
        self.max_workers = 20 # Scaled up for a larger army

    def create_batch_accounts(self, count, custom_specs=None):
        """
        FIXED: Now handles both simple numbers and hybrid country specs.
        Prevents 500 Internal Server Errors.
        """
        from identity_generator import IdentityGenerator
        id_gen = IdentityGenerator()
        
        try:
            # اگر custom_specs (جیسے UK:10) ملے ہیں، تو ان کے مطابق جنریٹ کرو
            if custom_specs and isinstance(custom_specs, dict):
                print(f"⚙️ Processing hybrid request: {custom_specs}")
                # identity_generator کو لسٹ بھیج رہے ہیں
                identities = id_gen.generate_batch(count, custom_specs=custom_specs)
            else:
                # اگر صرف سادہ نمبر ہے، تو عام طریقے سے جنریٹ کرو
                print(f"⚙️ Processing simple request for {count} accounts")
                identities = id_gen.generate_batch(count)
            
            # اکاؤنٹس کو سیو کریں
            if identities:
                for identity in identities:
                    self.acc_manager.save_account(identity)
                print(f"✅ Successfully created and saved {len(identities)} accounts.")
            else:
                print("⚠️ No identities were generated.")
                
        except Exception as e:
            print(f"❌ CRITICAL ENGINE ERROR during creation: {e}")
            # یہاں ہم ایرر کو پرنٹ کریں گے تاکہ سرور کریش نہ ہو بلکہ لاگز میں نظر آئے

    def run_account_cycle(self, username):
        """
        The 'Human Chaos' Logic: No two accounts behave the same.
        """
        from uploader import TrustBuilder 
        builder = TrustBuilder(self)
        
        while True:
            accounts = self.acc_manager.get_all_accounts()
            acc_data = accounts.get(username)
            if not acc_data: break
            
            status = acc_data.get('status', 'Active')
            
            if status == 'Terminated': break
            if status == 'Paused':
                time.sleep(60) 
                continue

            initial_delay = random.randint(1, 3600) 
            time.sleep(initial_delay)

            try:
                behavior_mode = random.choice(['aggressive', 'passive', 'curious', 'minimal'])
                print(f"👤 {username} is now awake. Mode: {behavior_mode}")
                builder.perform_human_actions(acc_data, mode=behavior_mode)
                
                current_score = acc_data.get('trust_score', 0)
                self.acc_manager.update_trust_score(username, current_score + random.randint(1, 5))

            except Exception as e:
                print(f"⚠️ {username} encountered an error: {e}")

            if status == 'Active':
                sleep_time = random.randint(600, 28800) 
            else: 
                sleep_time = random.randint(7200, 86400) 
            
            print(f"💤 {username} is going to sleep for {sleep_time // 60} minutes.")
            time.sleep(sleep_time)

    def start_army(self):
        accounts = self.acc_manager.get_all_accounts()
        for username in accounts:
            if accounts[username].get('status') != 'Terminated':
                t = threading.Thread(target=self.run_account_cycle, args=(username,))
                t.daemon = True
                t.start()

    def boost_main_account(self, accounts, main_url):
        from traffic_pipeline import TrafficPipeline
        traffic = TrafficPipeline(self)
        traffic.route_traffic(main_url, accounts, mode="main")

    def get_system_status(self):
        accounts = self.acc_manager.get_all_accounts()
        return {"total_accounts": len(accounts), "system_health": "Ultra-Stealth", "engine_status": "Active"}
