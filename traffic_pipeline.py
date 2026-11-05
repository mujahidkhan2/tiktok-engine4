import random
import time
from datetime import datetime

class TrafficPipeline:
    def __init__(self, engine):
        self.engine = engine

    def route_traffic(self, target_url, worker_accounts, mode="main"):
        """
        mode="main": صرف مین اکاؤنٹ کو بوسٹ کرے گا
        mode="mutual": ورکر اکاؤنٹس ایک دوسرے کو سپورٹ کریں گے
        """
        random.shuffle(worker_accounts)
        
        for account in worker_accounts:
            wait_time = random.uniform(60, 600)
            # Mutual Support Logic: اگر موڈ میوچل ہے تو کچھ اکاؤنٹس دوسرے ورکرز کی ویڈیوز دیکھیں گے
            if mode == "mutual":
                print(f"Account {account['id']} is supporting a fellow worker account...")
            
            self.execute_human_interaction(account, target_url)

    def execute_human_interaction(self, account, video_url):
        """انسانی رویہ: دیکھنا، رکنا، لائک کرنا اور کمنٹ کرنا"""
        actions = ["watch_full", "watch_half_then_like", "like_and_comment", "just_watch"]
        chosen_action = random.choice(actions)
        
        # وقت کا وقفہ تاکہ مشین نہ لگے
        if chosen_action == "watch_full":
            time.sleep(random.uniform(15, 30))
        elif chosen_action == "watch_half_then_like":
            time.sleep(random.uniform(5, 12))
        
        if random.random() < 0.15: # 15% چانس کمنٹ کرنے کا
            print(f"Account {account['id']} is engaging to increase mutual value...")