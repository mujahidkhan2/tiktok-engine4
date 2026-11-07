import random
import time
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.active = True

    def human_sleep_pattern(self, mode="standard"):
        """Implements non-linear, chaotic human timing"""
        hour = datetime.now().hour
        
        # Night mode: Long sleeps, very few actions
        if 0 <= hour <= 6: 
            patterns = [(600, 3600), (1800, 7200)]
            weight = [70, 30]
        # Day mode: Mixed activities
        else: 
            # Randomize: some act fast, some very slow (Human nature)
            patterns = [(10, 60), (300, 900), (1800, 3600), (1, 5)]
            weight = [40, 30, 20, 10]
            
        choice = random.choices(patterns, weights=weight)[0]
        sleep_time = random.uniform(choice[0], choice[1])
        time.sleep(sleep_time)

    def schedule_task(self, task_func, *args):
        if self.active:
            self.human_sleep_pattern()
            return task_func(*args)
        return None