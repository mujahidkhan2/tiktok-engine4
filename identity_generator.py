import random
import uuid
import hashlib

class IdentityGenerator:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
        ]

    def generate_device_fingerprint(self):
        # رینڈم ڈیوائس آئی ڈی بنانا تاکہ ہر اکاؤنٹ کی شناخت الگ ہو
        device_id = str(uuid.uuid4())
        canvas_id = hashlib.sha256(str(random.random()).encode()).hexdigest()[:16]
        return {
            "device_id": device_id,
            "canvas_id": canvas_id,
            "user_agent": random.choice(self.user_agents),
            "screen_res": random.choice(["1920x1080", "1366x768", "390x844", "414x896"])
        }

    def create_stealth_profile(self, country):
        # ملک کے حساب سے پروفائل سیٹنگز
        return {
            "country": country,
            "timezone": self._get_timezone(country),
            "language": self._get_language(country),
            "fingerprint": self.generate_device_fingerprint()
        }

    def _get_timezone(self, country):
        tz_map = {"UK": "GMT", "USA": "EST", "SAUDI": "AST", "UAE": "GST", "PK": "PKT", "IN": "IST"}
        return tz_map.get(country, "UTC")

    def _get_language(self, country):
        lang_map = {"UK": "en-GB", "USA": "en-US", "SAUDI": "ar-SA", "UAE": "ar-AE", "PK": "ur-PK", "IN": "en-IN"}
        return lang_map.get(country, "en-US")
