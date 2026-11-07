import random
import uuid
import hashlib

class IdentityGenerator:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
        ]

    def generate_device_fingerprint(self):
        return {
            "device_id": str(uuid.uuid4()),
            "canvas_id": hashlib.sha256(str(random.random()).encode()).hexdigest()[:16],
            "user_agent": random.choice(self.user_agents),
            "screen_res": random.choice(["1920x1080", "1366x768", "390x844", "414x896"]),
            "gpu": random.choice(["NVIDIA GeForce RTX 3060", "Intel Iris Xe", "Apple M2", "Adreno 650"])
        }

    def create_stealth_profile(self, country):
        # Category-based Persona matching
        categories = ["Tech", "Gaming", "Vlog", "Funny", "Education"]
        selected_cat = random.choice(categories)
        
        return {
            "country": country,
            "category": selected_cat,
            "timezone": self._get_timezone(country),
            "language": self._get_language(country),
            "fingerprint": self.generate_device_fingerprint(),
            "bio": f"Professional {selected_cat} enthusiast from {country}",
            "profile_pic_type": f"{selected_cat}_themed_random"
        }

    def _get_timezone(self, country):
        tz_map = {"UK": "GMT", "USA": "EST", "SAUDI": "AST", "UAE": "GST", "PK": "PKT", "IN": "IST"}
        return tz_map.get(country, "UTC")

    def _get_language(self, country):
        lang_map = {"UK": "en-GB", "USA": "en-US", "SAUDI": "ar-SA", "UAE": "ar-AE", "PK": "ur-PK", "IN": "en-IN"}
        return lang_map.get(country, "en-US")
