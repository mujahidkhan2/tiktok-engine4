import random
import time
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.active = True

    def get_random_delay(self, min_s=5, max_s=30):
        # ریاضیاتی وقفہ تاکہ مشین جیسا پیٹرن نہ بنے
        return random.uniform(min_s, max_s)

    def human_sleep_pattern(self):
        # انسانوں کی طرح کبھی لمبا وقفہ، کبھی چھوٹا
        patterns = [
            (10, 60),   # عام وقفہ
            (300, 900), # لمبا وقفہ (بریک)
            (1, 10)     # تیز رفتار کام
        ]
        choice = random.choices(patterns, weights=[70, 20, 10])[0]
        time.sleep(random.uniform(choice[0], choice[1]))

    def schedule_task(self, task_func, *args):
        # کسی بھی کام کو رینڈم وقت پر چلانا
        if self.active:
            self.human_sleep_pattern()
            return task_func(*args)
        return None
