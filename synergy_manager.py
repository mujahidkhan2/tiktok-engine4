import random
import time
from concurrent.futures import ThreadPoolExecutor

class SynergyManager:
    def __init__(self, engine):
        self.engine = engine

    def coordinate_workers(self):
        all_accs = list(self.engine.acc_manager.get_all_accounts().keys())
        random.shuffle(all_accs)
        return [all_accs[i:i + 5] for i in range(0, len(all_accs), 5)]

    def run_growth_cycle(self, batches):
        with ThreadPoolExecutor(max_workers=2) as executor:
            for batch in batches:
                executor.submit(self._execute_mutual_support, batch)
                time.sleep(random.uniform(10, 30))

    def _execute_mutual_support(self, batch):
        for user in batch:
            try:
                time.sleep(random.uniform(15, 40))
                # Mutual action simulation
            except Exception:
                pass