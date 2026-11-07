import random

class HealthTracker:
    def __init__(self):
        self.health_logs = {}
        self.ban_reasons_history = []

    def check_shop_eligibility(self, account_id):
        # Simulating trust score and engagement for shop eligibility
        metrics = {
            "trust_score": random.uniform(0, 100),
            "engagement_rate": random.uniform(0.1, 5.0),
            "follower_count": random.randint(10, 1500),
            "shadowban": random.random() < 0.03
        }
        
        # Eligibility logic: High trust, no shadowban, and minimum engagement
        is_eligible = not metrics["shadowban"] and metrics["trust_score"] > 75 and metrics["follower_count"] >= 1000
        self.health_logs[account_id] = {"eligible": is_eligible, "metrics": metrics}
        return is_eligible

    def analyze_rejection(self, account_id):
        """Analyses why an account was banned or rejected for shop"""
        reasons = [
            "Low Engagement/Trust Score", 
            "Residential Proxy Flagged", 
            "Content Quality (Duplicate/Low)", 
            "Device Fingerprint Mismatch", 
            "Aggressive Following Pattern",
            "Excessive Liking/Commenting"
        ]
        reason = random.choice(reasons)
        self.ban_reasons_history.append({"account": account_id, "reason": reason})
        return reason

    def get_ban_trend(self):
        """Returns the most common reason for bans to help the engine adjust"""
        if not self.ban_reasons_history:
            return "No bans recorded."
        reasons = [r["reason"] for r in self.ban_reasons_history]
        return max(set(reasons), key=reasons.count)