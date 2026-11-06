import os
import threading
import time
from flask import Flask, render_template_string
from identity_generator import IdentityGenerator
from account_manager import AccountManager
from engine import Engine
from synergy_manager import SynergyManager
from traffic_pipeline import TrafficPipeline
from scheduler import Scheduler
from video_creator import VideoCreator
from uploader import StealthUploader
from health_tracker import HealthTracker

app = Flask(__name__)

# --- GLOBAL SYSTEM STATE (ڈیش بورڈ کے لیے ڈیٹا) ---
stats = {
    "total_accounts": 0,
    "active": 0,
    "paused": 0,
    "terminated": 0,
    "shop_eligible": 0,
    "progress": 0,
    "current_action": "System Idle",
    "logs": []
}

class TikTokMasterEngine:
    def __init__(self):
        self.id_gen = IdentityGenerator()
        self.acc_manager = AccountManager()
        self.engine = Engine(self.id_gen, self.acc_manager)
        self.synergy = SynergyManager()
        self.traffic = TrafficPipeline()
        self.scheduler = Scheduler()
        self.video_gen = VideoCreator()
        self.uploader = StealthUploader(self.id_gen)
        self.health = HealthTracker()
        self.is_running = False

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        stats["logs"].insert(0, f"[{timestamp}] {message}")
        if len(stats["logs"]) > 15: stats["logs"].pop()

    def execute_stealth_workflow(self, country_config):
        """سرور کو کریش سے بچانے کے لیے 'بیچ' (Batch) سسٹم"""
        self.is_running = True
        total_target = sum(country_config.values())
        processed = 0

        for country, count in country_config.items():
            for i in range(count):
                if not self.is_running: break
                
                stats["current_action"] = f"Processing {country} Account {i+1}/{count}"
                
                # 1. اکاؤنٹ کریشن (Low Pressure Mode)
                account_id = self.engine.create_account(country)
                if account_id:
                    stats["total_accounts"] += 1
                    stats["active"] += 1
                    self.log(f"Created {account_id} ({country})")
                    
                    # 2. انسانی رویوں کا وقفہ (Anti-Detection)
                    self.scheduler.apply_human_delay()
                    self.traffic.route_smart_traffic(account_id)
                    
                    # 3. AI مواد اور اپلوڈ
                    video_data = self.video_gen.create_unique_video_metadata(account_id, country)
                    if self.uploader.upload_video(account_id, video_data):
                        self.log(f"Uploaded content for {account_id}")
                    
                    # 4. ہیلتھ چیک اور شاپ ایلیجیبلٹی
                    if self.health.check_shop_eligibility(account_id):
                        stats["shop_eligible"] += 1
                        self.log(f"⭐ {account_id} is SHOP ELIGIBLE!")
                    
                    self.synergy.add_to_cluster(account_id, country)
                    
                    processed += 1
                    stats["progress"] = int((processed / total_target) * 100)
                    
                    # سرور ریلیف (Cool-down period) - تاکہ سرور کو محسوس نہ ہو
                    time.sleep(random.uniform(2, 5)) 
                else:
                    stats["terminated"] += 1
                    self.log(f"⚠️ Account creation failed for {country}")

        stats["current_action"] = "Workflow Completed"
        self.is_running = False

# انجن کا انسٹنس
master_bot = TikTokMasterEngine()

# --- DASHBOARD HTML (پاور فل اور جدید) ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>TikTok Engine 4 - Master Dashboard</title>
    <style>
        body { background: #0f0f0f; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .card h3 { margin: 0; font-size: 14px; color: #888; text-transform: uppercase; }
        .card p { margin: 10px 0 0; font-size: 28px; font-weight: bold; color: #00ffcc; }
        .progress-container { background: #222; border-radius: 20px; height: 25px; width: 100%; margin: 20px 0; position: relative; border: 1px solid #444; }
        .progress-bar { background: linear-gradient(90deg, #00ffcc, #0088ff); height: 100%; border-radius: 20px; width: {{progress}}%; transition: width 0.5s; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 2px; font-size: 14px; font-weight: bold; }
        .log-box { background: #000; border: 1px solid #333; border-radius: 10px; padding: 15px; height: 300px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 13px; color: #00ff00; }
        .status-banner { background: #1a1a1a; padding: 10px 20px; border-radius: 10px; border-right: 5px solid #00ffcc; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        .btn { background: #00ffcc; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="status-banner">
        <span><strong>سسٹم اسٹیٹس:</strong> {{current_action}}</span>
        <a href="/start" class="btn">انجن شروع کریں 🚀</a>
    </div>

    <div class="grid">
        <div class="card"><h3>کل اکاؤنٹس</h3><p>{{total}}</p></div>
        <div class="card"><h3>ایکٹو (Active)</h3><p>{{active}}</p></div>
        <div class="card"><h3>ناکام (Terminated)</h3><p>{{terminated}}</p></div>
        <div class="card"><h3>شاپ ایلیجیبل ✅</h3><p>{{eligible}}</p></div>
    </div>

    <div class="progress-container">
        <div class="progress-bar" style="width: {{progress}}%"></div>
        <div class="progress-text">مکمل tiến: {{progress}}%</div>
    </div>

    <h3>لائیو لاگز (Real-time Logs)</h3>
    <div class="log-box">
        {% for log in logs %}<div style="margin-bottom:5px;">{{log}}</div>{% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(
        DASHBOARD_HTML, 
        total=stats["total_accounts"], 
        active=stats["active"], 
        terminated=stats["terminated"], 
        eligible=stats["shop_eligible"], 
        progress=stats["progress"], 
        current_action=stats["current_action"],
        logs=stats["logs"]
    )

@app.route('/start')
def start_engine():
    if not master_bot.is_running:
        # بیک گراؤنڈ میں انجن چلانے کے لیے Thread استعمال کریں تاکہ ڈیش بورڈ ہینگ نہ ہو
        config = {"UK": 10, "USA": 10} # یہاں اپنی تعداد لکھیں
        thread = threading.Thread(target=master_bot.execute_stealth_workflow, args=(config,))
        thread.start()
        return "انجن شروع ہو گیا ہے! ڈیش بورڈ چیک کریں۔"
    return "انجن پہلے سے چل رہا ہے!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
