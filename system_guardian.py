import logging
import time
from datetime import datetime

class SystemGuardian:
    def __init__(self, master_bot):
        self.master_bot = master_bot
        self.recovery_logs = []

    def monitor_health(self):
        """پورے سسٹم کے تمام ماڈیولز کو چیک کرتا ہے"""
        issues_found = []
        modules = self.master_bot.modules
        
        # تمام ضروری ماڈیولز کی موجودگی چیک کریں
        required = ['engine', 'acc_manager', 'id_gen', 'scheduler', 'uploader', 'health']
        for mod in required:
            if mod not in modules:
                issues_found.append(f"CRITICAL: {mod} module is missing!")
        
        return issues_found

    def attempt_recovery(self, module_name):
        """اگر کوئی ماڈیول کریش ہو جائے تو اسے دوبارہ لوڈ کرنے کی کوشش کرتا ہے"""
        try:
            logging.info(f"Attempting to recover {module_name}...")
            self.master_bot.load_modules() 
            return True
        except Exception as e:
            logging.error(f"Recovery failed for {module_name}: {e}")
            return False

    def analyze_account_failure(self, account_id, error_msg):
        """اکاؤنٹ کی ناکامی کی وجہ نکال کر حل تجویز کرتا ہے"""
        solution = "Unknown"
        if "Proxy" in error_msg:
            solution = "Change Proxy IP / Rotate Gateway"
        elif "Fingerprint" in error_msg:
            solution = "Update Device ID in Identity Generator"
        elif "Limit" in error_msg:
            solution = "Increase Human Delay in Scheduler"
        
        report = f"[{datetime.now()}] Acc: {account_id} | Err: {error_msg} | Sol: {solution}"
        self.recovery_logs.append(report)
        return report