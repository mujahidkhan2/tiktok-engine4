import json
import os

class AccountManager:
    def __init__(self, storage_file="accounts_data.json"):
        self.storage_file = storage_file
        self.accounts = self._load_accounts()

    def _load_accounts(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # اگر ڈیٹا لسٹ میں ہے تو اسے ڈکشنری میں تبدیل کریں تاکہ main.py کے ساتھ میچ کرے
                    if isinstance(data, list):
                        return {acc['username']: acc for acc in data}
                    return data
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_account(self, account_info):
        # اکاؤنٹ کی مکمل پروفائلنگ (Trust Score اور Status کے ساتھ)
        username = account_info.get('username')
        if not username:
            return False
            
        # ڈیفالٹ ویلیوز جو الگورتھم کو بیfool کرنے کے لیے ضروری ہیں
        account_info.setdefault("status", "Active")
        account_info.setdefault("trust_score", 0)
        account_info.setdefault("device_id", "Unknown")
        account_info.setdefault("video_links", [])
        account_info.setdefault("last_activity", "None")
        
        self.accounts[username] = account_info
        self._write_to_file()
        return True

    def update_status(self, username, new_status):
        # بجلی کی رفتار سے اسٹیٹس اپڈیٹ (Dictionary Lookup)
        if username in self.accounts:
            self.accounts[username]['status'] = new_status
            self._write_to_file()
            return True
        return False

    def update_trust_score(self, username, score):
        # ٹرسٹ سکور اپڈیٹ کرنے کے لیے (تاکہ پتہ چلے اکاؤنٹ کب VIP بنے گا)
        if username in self.accounts:
            self.accounts[username]['trust_score'] = score
            self._write_to_file()

    def _write_to_file(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.accounts, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"❌ ڈیٹا سیو کرنے میں غلطی: {e}")

    def get_all_accounts(self):
        # یہ اب ایک ڈکشنری واپس کرے گا جو main.py کے ٹیبل کے لیے پرفیکٹ ہے
        return self.accounts

    def clear_all_accounts(self):
        self.accounts = {}
        self._write_to_file()