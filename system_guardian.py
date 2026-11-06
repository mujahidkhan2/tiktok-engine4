### 10. فائل کا نام: `system_guardian.py` 🚨 (نیو فائل - New File)
**(اسے ایک نئی فائل کے طور پر بنائیں اور یہ کوڈ ڈالیں)**

```python
import logging
import time
from datetime import datetime

class SystemGuardian:
    def __init__(self, master\_bot):
        self.master\_bot = master\_bot
        self.recovery\_logs = []

    def monitor\_health(self):
        """پورے سسٹم کے تمام ماڈیولز کو چیک کرتا ہے"""
        issues\_found = []
        modules = self.master\_bot.modules
        
        # تمام ضروری ماڈیولز کی موجودگی چیک کریں
        required = ['engine', 'acc\_manager', 'id\_gen', 'scheduler', 'uploader', 'health']
        for mod in required:
            if mod not in modules:
                issues\_found.append(f"CRITICAL: {mod} module is missing!")
        
        return issues\_found

    def attempt\_recovery(self, module\_name):
        """اگر کوئی ماڈیول کریش ہو جائے تو اسے دوبارہ لوڈ کرنے کی کوشش کرتا ہے"""
        try:
            logging.info(f"Attempting to recover {module\_name}...")
            self.master\_bot.load\_modules() 
            return True
        except Exception as e:
            logging.error(f"Recovery failed for {module\_name}: {e}")
            return False

    def analyze\_account\_failure(self, account\_id, error\_msg):
        """اکاؤنٹ کی ناکامی کی وجہ نکال کر حل تجویز کرتا ہے"""
        solution = "Unknown"
        if "Proxy" in error\_msg:
            solution = "Change Proxy IP / Rotate Gateway"
        elif "Fingerprint" in error\_msg:
            solution = "Update Device ID in Identity Generator"
        elif "Limit" in error\_msg:
            solution = "Increase Human Delay in Scheduler"
        
        report = f"[{datetime.now()}] Acc: {account\_id} | Err: {error\_msg} | Sol: {solution}"
        self.recovery\_logs.append(report)
        return report
