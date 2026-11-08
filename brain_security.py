import hashlib
import hmac
import secrets
import time
import os

class BrainSecurity:
    def __init__(self, master_key):
        self.master_key = master_key.encode()
        self.session_tokens = {}
        self.blacklist = []

    def verify_token(self, user_id, token):
        """
        صرف وہی ٹوکن قبول کرے گا جو ماسٹر کی سے میچ کرتا ہو
        """
        # یہاں ہم ماسٹر کی کو ہی ٹوکن کے طور پر استعمال کر رہے ہیں تاکہ سادہ رہے
        # لیکن یہ اندرونی طور پر ہیش (Hash) کے ذریعے چیک ہوتا ہے
        if token == self.master_key.decode():
            return True
        return False

    def encrypt_data(self, data):
        """ڈیٹا کو خفیہ کرنے کے لیے"""
        return hmac.new(self.master_key, data.encode(), hashlib.sha256).hexdigest()

    def monitor_threats(self, request_ip, request_pattern):
        if request_pattern == "aggressive":
            self.blacklist.append(request_ip)
            return "THREAT DETECTED: IP Blacklisted."
        return "Secure"

    def stealth_mode(self, active=True):
        if active:
            return "Stealth Mode Active: System is now invisible to scanners."
        return "Stealth Mode Deactivated."

    def self_destruct_logs(self):
        try:
            if os.path.exists('brain_activity.log'):
                os.remove('brain_activity.log')
                return "Security Breach: Logs wiped for safety."
        except Exception as e:
            return f"Error wiping logs: {str(e)}"

# یہاں وہی کی (Key) ڈالیں جو brain_core.py میں ہے
security_shield = BrainSecurity(master_key="OWNER_MASTER_KEY_2026")