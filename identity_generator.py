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

    def generate_identity(self, country=None):
        """
        Generates a single random identity.
        If country is provided, it uses that; otherwise, it uses Auto Mode.
        """
        if country is None:
            country = self.get_random_country()
            
        return {
            "country": country,
            "device_id": f"DEV_{random.getrandbits(32)}",
            "fingerprint": f"FP_{random.getrandbits(64)}",
            "proxy_type": "Residential" if country in ["UK", "USA"] else "Datacenter"
        }

    def generate_batch(self, count, custom_specs=None):
        """
        Robust Batch Generator:
        Handles: 
        1. Simple count (Auto Mode)
        2. Custom Specs (Manual Mode e.g., {"UK": 10, "USA": 5})
        """
        identities = []
        
        try:
            # Case 1: Manual Mode (Specific countries and counts)
            if custom_specs and isinstance(custom_specs, dict):
                print(f"📦 Generating batch with custom specs: {custom_specs}")
                for country, num in custom_specs.items():
                    # Ensure 'num' is an integer to prevent crashes
                    try:
                        valid_num = int(num)
                        for _ in range(valid_num):
                            identities.append(self.generate_identity(country=country))
                    except (ValueError, TypeError):
                        print(f"⚠️ Skipping invalid number for {country}: {num}")
                
                # If for some reason no identities were created from specs, 
                # fall back to auto-mode to prevent 500 error.
                if not identities:
                    for _ in range(count):
                        identities.append(self.generate_identity())
                        
            # Case 2: Auto Mode (Only total count provided)
            else:
                print(f"📦 Generating batch in auto-mode for {count} accounts")
                for _ in range(count):
                    identities.append(self.generate_identity())
                    
        except Exception as e:
            print(f"❌ Critical error in generate_batch: {e}")
            # Final fallback: return at least some identities to prevent server crash
            for _ in range(count if isinstance(count, int) else 1):
                identities.append(self.generate_identity())
        
        return identities
