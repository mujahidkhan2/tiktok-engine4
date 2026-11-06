import random

class HealthTracker:
    def __init__(self):
        self.health_logs = {}

    def check_shop_eligibility(self, account_id):
        """اکاؤنٹ کی ہیلتھ اور شاپ ایلیجیبلٹی چیک کرتا ہے"""
        # حقیقت میں یہاں API کال ہوگی، فی الحال لاجک سیمولیشن ہے
        metrics = {
            "engagement_rate": random.uniform(0.1, 5.0),
            "follower_count": random.randint(10, 1000),
            "shadowban_status": random.choice([True, False]) if random.random() < 0.05 else False
        }
        
        # شاپ ایلیجیبلٹی کی شرط: کوئی شیڈو بین نہ ہو اور انگیجمنٹ 1.0 سے اوپر ہو
        is_eligible = not metrics["shadowban_status"] and metrics["engagement_rate"] > 1.0
        
        self.health_logs[account_id] = {
            "eligible": is_eligible,
            "metrics": metrics
        }
        
        status = "ELIGIBLE ✅" if is_eligible else "NOT ELIGIBLE ❌"
        print(f"[HealthTracker] Account {account_id} Status: {status}")
        return is_eligible

    def analyze_rejection(self, account_id):
        """اگر اکاؤنٹ ریجیکٹ ہوا تو اس کی وجہ بتاتا ہے"""
        reasons = ["Low Engagement", "Proxy Detection", "Content Duplicate", "Device Fingerprint Match"]
        return random.choice(reasons)
