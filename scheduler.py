import random
import time
from datetime import datetime, timedelta

class Scheduler:
    def __init__(self):
        # انسانی رویے کے مختلف پیٹرنز (مثلاً کچھ لوگ صبح جلدی جاگتے ہیں، کچھ دیر سے)
        self.behavior_profiles = ["early_bird", "night_owl", "balanced", "irregular"]

    def get_staggered_delay(self, account_index):
        """
        تاکہ 100 اکاؤنٹس ایک ساتھ ایکٹو نہ ہوں بلکہ ایک ایک کر کے شروع ہوں
        """
        # ہر اکاؤنٹ کے درمیان 30 سیکنڈ سے 3 منٹ کا رینڈم فرق
        return random.uniform(30, 180) * (account_index + 1)

    def get_random_interval(self, min_val, max_val):
        """مختلف ایکشنز کے درمیان رینڈم وقفہ"""
        return random.uniform(min_val, max_val)

    def wait_for_step(self, step_name, min_min=1, max_min=5):
        """سٹیپس کے درمیان انسانی وقفہ"""
        wait_time = random.uniform(min_min * 60, max_min * 60)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Humanizing: Waiting {round(wait_time/60, 2)} mins for {step_name}...")
        time.sleep(wait_time)

    def get_sleep_cycle(self, profile=None):
        """
        ہر اکاؤنٹ کا سونے اور جاگنے کا وقت مختلف ہوگا
        """
        if not profile:
            profile = random.choice(self.behavior_profiles)
        
        if profile == "early_bird":
            start, end = random.randint(5, 8), random.randint(21, 23)
        elif profile == "night_owl":
            start, random_end = random.randint(13, 16), random.randint(1, 4)
        elif profile == "balanced":
            start, end = random.randint(8, 10), random.randint(22, 0)
        else: # irregular
            start, end = random.randint(6, 18), random.randint(20, 5)

        return {
            "profile": profile,
            "active_start": start,
            "active_end": end,
            "is_awake": False
        }

    def should_be_active(self, sleep_cycle):
        """چیک کرتا ہے کہ کیا اس وقت اکاؤنٹ کو جاگنا چاہیے یا سونا چاہیے"""
        current_hour = datetime.now().hour
        start = sleep_cycle["active_start"]
        end = sleep_cycle["active_end"]

        if start <= end:
            return start <= current_hour < end
        else: # اگر سونا رات 12 بجے کے بعد ہو (Cross-midnight)
            return current_hour >= start or current_hour < end