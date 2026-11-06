import random

class HealthTracker:
    def __init__(self):
        self.health_logs = {}

    def check_shop_eligibility(self, account_id):
        metrics = {
            "engagement_rate": random.uniform(0.1, 5.0),
            "follower_count": random.randint(10, 1000),
            "shadowban": random.random() < 0.03
        }
        
        is_eligible = not metrics["shadowban"] and metrics["engagement_rate"] > 1.2
        self.health_logs[account_id] = {"eligible": is_eligible, "metrics": metrics}
        return is_eligible

    def analyze_rejection(self, account_id):
        reasons = ["Low Engagement", "Proxy Flagged", "Content Quality Low", "Device Mismatch"]
        return random.choice(reasons)
