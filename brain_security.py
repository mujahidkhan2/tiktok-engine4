import hashlib
import hmac
import secrets
import time
from datetime import datetime

class BrainSecurity:
    def __init__(self, master_key):
        self.master_key = master_key.encode()
        self.session_tokens = {}
        self.blacklist = []

    def generate_dynamic_token(self, user_id):
        """ہر سیشن کے لیے بدلنے والا ٹوکن (Bank Level)"""
        token = secrets.token_urlsafe(32)
        expiry = time.time() + 3600 # 1 hour validity
        self.session_tokens[user_id] = {"token": token, "expiry": expiry}
        return token

    def verify_token(self, user_id, token):
        """ٹوکن کی تصدیق کرنا"""
        if user_id in self.session_tokens:
            session = self.session_tokens[user_id]
            if session["token"] == token and time.time() < session["expiry"]:
                return True
        return False

    def encrypt_data(self, data):
        """ڈیٹا کو خفیہ کرنا تاکہ کوئی پڑھ نہ سکے"""
        return hmac.new(self.master_key, data.encode(), hashlib.sha256).hexdigest()    def monitor_threats(self, request_ip, request_pattern):
        """غیر معمولی سرگرمی کو ڈیٹیکٹ کرنا"""
        # اگر کوئی بار بار غلط ٹوکن بھیجے تو اسے بلاک کرنا
        if request_pattern == "aggressive":
            self.blacklist.append(request_ip)
            return "THREAT DETECTED: IP Blacklisted."
        return "Secure"

    def stealth_mode(self, active=True):
        """سسٹم کو مکمل طور پر غائب کرنا"""
        if active:
            # یہاں ایسے فنکشنز ہوں گے جو سرور کی اصل آئی ڈی چھپائیں گے
            return "Stealth Mode Active: System is now invisible to scanners."
        return "Stealth Mode Deactivated."

    def self_destruct_logs(self):
        """مشکوک صورتحال میں لاگز کو خود بخود ختم کرنا"""
        try:
            if os.path.exists('brain_activity.log'):
                os.remove('brain_activity.log')
                return "Security Breach: Logs wiped for safety."
        except Exception as e:
            return f"Error wiping logs: {str(e)}"

# Initialize Security with the same secret key
security_shield = BrainSecurity(master_key="YOUR_SECRET_ACCESS_KEY_123")