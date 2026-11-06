import json
import os
import logging
from threading import Lock

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='system_logs.log')

class AccountManager:
    def __init__(self, storage_file="accounts_db.json"):
        self.storage_file = storage_file
        self.lock = Lock()
        self.accounts = self.load_accounts()

    def load_accounts(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Database Load Error: {e}")
            return {}

    def save_accounts(self):
        try:
            with self.lock:
                with open(self.storage_file, "w", encoding="utf-8") as f:
                    json.dump(self.accounts, f, indent=4)
        except Exception as e:
            logging.error(f"Database Save Error: {e}")

    def add_account(self, username, details):
        try:
            self.accounts[username] = details
            self.save_accounts()
            return True
        except Exception as e:
            logging.error(f"Add Account Error: {e}")
            return False

    def update_status(self, username, status):
        if username in self.accounts:
            self.accounts[username]["status"] = status
            self.save_accounts()
            return True
        return False

    def get_all_accounts(self):
        return self.accounts

    def export_account_data(self, username):
        """اکاؤنٹ کا مکمل ڈیٹا نکالنے کے لیے (Sell-Ready Feature)"""
        return self.accounts.get(username, "Account not found")

    def clear_all_accounts(self):
        with self.lock:
            self.accounts = {}
            if os.path.exists(self.storage_file):
                os.remove(self.storage_file)
