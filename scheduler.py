import random
import time
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.active = True

    def human_sleep_pattern(self):
        # دن اور رات کے حساب سے وقفہ
        hour = datetime.now().hour
        if 0 <= hour <= 6: # رات کا وقت: لمبا وقفہ
            patterns = [(300, 1800), (600, 3600)]
            weight = [80, 20]
        else: # دن کا وقت: متوازن وقفہ
            patterns = [(10, 60), (300, 900), (1, 10)]
            weight = [70, 20, 10]
            
        choice = random.choices(patterns, weights=weight)[0]
        time.sleep(random.uniform(choice[0], choice[1]))

    def schedule_task(self, task_func, *args):
        if self.active:
            self.human_sleep_pattern()
            return task_func(*args)
        return None
