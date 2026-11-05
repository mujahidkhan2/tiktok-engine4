import json
from datetime import datetime

class HealthTracker:
    def __init__(self, accounts_file='accounts_data.json'):
        self.accounts_file = accounts_file

    def load_accounts(self):
        try:
            with open(self.accounts_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading accounts: {e}")
            return []

    def generate_detailed_report(self):
        """
        پروفیشنل بزنس رپورٹ: کتنے کامیاب، کتنے خطرے میں اور کتنے فروخت کے لیے تیار
        """
        accounts = self.load_accounts()
        report = {
            "summary": {
                "total": len(accounts),
                "healthy": 0,
                "warning": 0, # وہ اکاؤنٹس جن کی گروتھ رک گئی ہے
                "banned": 0,
                "vip_sellable": 0
            },
            "sellable_list": [],
            "risk_list": []
        }

        for acc in accounts:
            status = acc.get('status', 'unknown')
            followers = acc.get('followers', 0)
            views = acc.get('total_views', 0)
            engagement = acc.get('engagement_rate', 0)

            if status == 'banned':
                report["summary"]["banned"] += 1
                report["risk_list"].append(acc['id'])
            
            elif status == 'active':
                # VIP Sellable Logic: اگر فالوورز 1k+ ہوں اور انگیجمنٹ اچھی ہو
                if followers >= 1000 and engagement > 5:
                    report["summary"]["vip_sellable"] += 1
                    report["sellable_list"].append({
                        "id": acc['id'], 
                        "value": "High", 
                        "metrics": f"F:{followers}, V:{views}"
                    })
                
                # Warning Logic: اگر اکاؤنٹ ایکٹو ہے پر ویوز بہت کم ہیں (Shadow Ban کا اشارہ)
                if views < 10 and followers < 10:
                    report["summary"]["warning"] += 1
                    report["risk_list"].append(acc['id'])
                else:
                    report["summary"]["healthy"] += 1

        return report

    def get_account_health_status(self, account_id):
        """کسی ایک مخصوص اکاؤنٹ کی گہری جانچ"""
        accounts = self.load_accounts()
        for acc in accounts:
            if acc['id'] == account_id:
                # لوجک: اگر ویوز فالوورز کے مقابلے میں بہت کم ہیں تو اسے 'Sick' قرار دیں
                f = acc.get('followers', 0)
                v = acc.get('total_views', 0)
                if f > 100 and v < (f * 0.1):
                    return "Sick (Low Reach) - Needs Warmup"
                return "Healthy"
        return "Not Found"

    def mark_as_banned(self, account_id):
        """اگر کوئی اکاؤنٹ پکڑا جائے تو اسے فوراً مارک کرنا تاکہ سسٹم اسے دوبارہ استعمال نہ کرے"""
        accounts = self.load_accounts()
        for acc in accounts:
            if acc['id'] == account_id:
                acc['status'] = 'banned'
                acc['banned_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        with open(self.accounts_file, 'w') as f:
            json.dump(accounts, f, indent=4)