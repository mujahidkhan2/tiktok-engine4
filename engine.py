import time
import random
from account\_manager import AccountManager
from identity\_generator import IdentityGenerator

class TikTokEngine:
    def __init__(self):
        self.acc\_manager = AccountManager()
        self.id\_gen = IdentityGenerator()

    def get\_identity(self, account\_id):
        """اکاؤنٹ کی شناخت واپس کرتا ہے (Uploader کے لیے)"""
        acc = self.acc\_manager.get\_all\_accounts().get(account\_id)
        return acc["profile"] if acc else {}

    def create\_account(self, country):
        try:
            profile = self.id\_gen.create\_stealth\_profile(country)
            username = f"user_{random.randint(100000, 999999)}_{country.lower()}"
            password = f"Pass_{random.randint(1000, 9999)}!_{country}"
            
            time.sleep(random.uniform(3, 7))
            
            account\_data = {
                "password": password,
                "country": country,
                "status": "warming",
                "profile": profile,
                "created\_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.acc\_manager.add\_account(username, account\_data)
            return username
        except Exception as e:
            return None
