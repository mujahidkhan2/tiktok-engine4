import json
import os

class AccountManager:
    def __init__(self, storage_file="accounts_db.json"):
        self.storage_file = storage_file
        self.accounts = self.load_accounts()

    def load_accounts(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                return json.load(f)
        return {}

    def save_accounts(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.accounts, f, indent=4)

    def add_account(self, username, details):
        self.accounts[username] = details
        self.save_accounts()

    def update_status(self, username, status):
        if username in self.accounts:
            self.accounts[username]["status"] = status
            self.save_accounts()
            return True
        return False

    def get_all_accounts(self):
        return self.accounts

    def clear_all_accounts(self):
        self.accounts = {}
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
