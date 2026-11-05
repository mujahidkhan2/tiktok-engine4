import random

class IdentityGenerator:
    def __init__(self):
        # Default Weights for Auto Mode
        self.default_weights = {
            "UK": 0.45,
            "USA": 0.35,
            "EU": 0.10,
            "Other": 0.10
        }
        self.other_countries = ["PK", "SA", "AE", "BD", "IN"]

    def get_random_country(self):
        """Auto Mode: Returns country based on weights"""
        r = random.random()
        if r < self.default_weights["UK"]:
            return "UK"
        elif r < self.default_weights["UK"] + self.default_weights["USA"]:
            return "USA"
        elif r < self.default_weights["UK"] + self.default_weights["USA"] + self.default_weights["EU"]:
            return "EU"
        else:
            return random.choice(self.other_countries)

    def generate_identity(self):
        """Generates a single random identity"""
        country = self.get_random_country()
        return {
            "country": country,
            "device_id": f"DEV_{random.getrandbits(32)}",
            "fingerprint": f"FP_{random.getrandbits(64)}",
            "proxy_type": "Residential" if country in ["UK", "USA"] else "Datacenter"
        }

    def generate_batch(self, count, custom_specs=None):
        """
        Handles both Auto and Manual modes.
        custom_specs example: {"UK": 5, "USA": 2, "PK": 1}
        """
        identities = []
        
        if custom_specs:
            # Manual Mode: Generate exact numbers as requested
            for country, num in custom_specs.items():
                for _ in range(num):
                    identities.append({
                        "country": country,
                        "device_id": f"DEV_{random.getrandbits(32)}",
                        "fingerprint": f"FP_{random.getrandbits(64)}",
                        "proxy_type": "Residential" if country in ["UK", "USA"] else "Datacenter"
                    })
        else:
            # Auto Mode: Generate based on percentages
            for _ in range(count):
                identities.append(self.generate_identity())
        
        return identities