import time
import random
from concurrent.futures import ThreadPoolExecutor

class TrafficPipeline:
    def __init__(self, engine):
        self.engine = engine

    def route_traffic(self, target_url, accounts):
        acc_list = list(accounts.keys())
        with ThreadPoolExecutor(max_workers=2) as executor:
            for user in acc_list:
                executor.submit(self._simulate_visit, user, target_url)
                time.sleep(random.uniform(40, 150))

    def _simulate_visit(self, user, url):
        try:
            time.sleep(random.randint(20, 60))
            if random.random() < 0.3:
                pass # Like simulated
        except Exception:
            pass
