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
        from identity_generator import IdentityGenerator
        id_gen = IdentityGenerator()
        identities = id_gen.generate_batch(count, custom_specs=custom_specs)
        for identity in identities:
            self.acc_manager.save_account(identity)

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

            # --- STEP 1: Random Wake-up Offset ---
            # تاکہ 1000 اکاؤنٹس ایک ساتھ نہ جاگیں، ہر ایک اپنے لیے ایک رینڈم شروعاتی وقت چنے
            initial_delay = random.randint(1, 3600) # 1 سیکنڈ سے 1 گھنٹے کے درمیان رینڈم وقفہ
            time.sleep(initial_delay)

            try:
                # --- STEP 2: Human Behavior Simulation ---
                # یہاں ہم 'uploader' کو بتائیں گے کہ اس اکاؤنٹ کے لیے آج کا "موڈ" کیا ہے
                behavior_mode = random.choice(['aggressive', 'passive', 'curious', 'minimal'])
                
                print(f"👤 {username} is now awake. Mode: {behavior_mode}")
                
                # TrustBuilder اب اس 'behavior_mode' کے مطابق کام کرے گا
                builder.perform_human_actions(acc_data, mode=behavior_mode)
                
                # ٹرسٹ سکور میں اضافہ
                current_score = acc_data.get('trust_score', 0)
                self.acc_manager.update_trust_score(username, current_score + random.randint(1, 5))

            except Exception as e:
                print(f"⚠️ {username} encountered an error: {e}")

            # --- STEP 3: Random Sleep Cycle (The 'Alt-Pulat' Logic) ---
            # ایک اکاؤنٹ 10 منٹ بعد سو سکتا ہے، دوسرا 5 گھنٹے بعد۔
            # اس سے کوئی ترتیب نہیں رہے گی، بالکل انسانوں کی طرح۔
            if status == 'Active':
                sleep_time = random.randint(600, 28800) # 10 منٹ سے 8 گھنٹے تک رینڈم نیند
            else: # Slow Mode
                sleep_time = random.randint(7200, 86400) # 2 گھنٹے سے 24 گھنٹے تک رینڈم نیند
            
            print(f"💤 {username} is going to sleep for {sleep_time // 60} minutes.")
            time.sleep(sleep_time)

    def start_army(self):
        accounts = self.acc_manager.get_all_accounts()
        # ThreadPool کے بجائے ہم ہر اکاؤنٹ کے لیے الگ تھریڈ چلائیں گے تاکہ وہ اپنی اپنی رینڈم ٹائمنگ پر چلیں
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