import time
import random
from concurrent.futures import ThreadPoolExecutor

class TrafficPipeline:
    def __init__(self, engine):
        self.engine = engine

    def route_traffic(self, target_url, accounts, mode="main"):
        # ٹریفک کو پائپ لائن کی طرح بھیجنا تاکہ اچانک سپائک (Spike) نہ آئے
        acc_list = list(accounts.keys())
        
        with ThreadPoolExecutor(max_workers=2) as executor: # بہت کم ورکرز تاکہ سرور محفوظ رہے
            for user in acc_list:
                executor.submit(self._simulate_visit, user, target_url)
                # رینڈم وقفہ تاکہ ٹریفک "قدرتی" لگے
                time.sleep(random.uniform(30, 120)) 

    def _simulate_visit(self, user, url):
        try:
            # ہیومن ویو ٹائم: صرف لنک کھولنا نہیں، بلکہ کچھ دیر رکنا
            view_time = random.randint(15, 45) 
            print(f"🚀 {user} is visiting {url} for {view_time}s...")
            time.sleep(view_time) 
            
            # رینڈم ایکشن: کچھ لوگ صرف دیکھیں گے، کچھ لائک کریں گے
            if random.random() < 0.3: # 30% چانس لائک کرنے کا
                print(f"❤️ {user} liked the content!")
        except Exception as e:
            print(f"Traffic Error for {user}: {e}")
