import os
import threading
import time
import random
from flask import Flask, render_template_string

# --- GLOBAL STATE ---
stats = {
    "total_accounts": 0, "active": 0, "paused": 0, "terminated": 0,
    "shop_eligible": 0, "progress": 0, "current_action": "System Ready", 
    "logs": [], "critical_errors": [] # یہاں تمام کمیاں جمع ہوں گی
}

app = Flask(__name__)

class SmartDiagnosticEngine:
    def __init__(self):
        self.modules = {}
        self.load_modules()

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        stats["logs"].insert(0, f"[{timestamp}] {message}")
        if len(stats["logs"]) > 20: stats["logs"].pop()

    def report_issue(self, file_name, error, solution):
        """یہ فنکشن سسٹم کی کمیاں نوٹ کرتا ہے تاکہ آپ اسے ٹھیک کر سکیں"""
        issue = f"❌ File: {file_name} | Error: {error} | Solution: {solution}"
        if issue not in stats["critical_errors"]:
            stats["critical_errors"].append(issue)
            self.log(f"🚨 SYSTEM ALERT: {file_name} needs attention!")

    def load_modules(self):
        """ہر فائل کو لوڈ کرنے کی کوشش، اگر کوئی مسنگ ہو تو اسے رپورٹ کرنا"""
        mapping = {
            'id_gen': ('identity_generator', 'IdentityGenerator', 'Check if identity_generator.py exists'),
            'acc_manager': ('account_manager', 'AccountManager', 'Check if account_manager.py exists'),
            'engine': ('engine', 'Engine', 'Check if engine.py is correct'),
            'scheduler': ('scheduler', 'Scheduler', 'Check if scheduler.py is correct'),
            'video_gen': ('video_creator', 'VideoCreator', 'Check if video_creator.py is correct'),
            'uploader': ('uploader', 'StealthUploader', 'Check if uploader.py is correct'),
            'health': ('health_tracker', 'HealthTracker', 'Check if health_tracker.py is correct')
        }

        for key, (file, cls, sol) in mapping.items():
            try:
                # ڈائنیمک امپورٹ تاکہ ایک فائل کی غلطی سے پورا سسٹم بند نہ ہو
                module = __import__(file)
                self.modules[key] = getattr(module, cls)()
            except Exception as e:
                self.report_issue(f"{file}.py", str(e), sol)

    def run_safe_workflow(self, country_config):
        self.is_running = True
        total_target = sum(country_config.values())
        processed = 0

        for country, count in country_config.items():
            for i in range(count):
                if not self.is_running: break
                stats["current_action"] = f"Processing {country} Account {i+1}/{count}"
                
                try:
                    # 1. اکاؤنٹ کریشن
                    if 'engine' not in self.modules: 
                        raise ImportError("Engine module not loaded. Cannot create accounts.")
                    
                    account_id = self.modules['engine'].create_account(country)
                    
                    if account_id:
                        stats["total_accounts"] += 1
                        stats["active"] += 1
                        self.log(f"✅ Created: {account_id}")
                        
                        # 2. وارم اپ - Fail Safe
                        try:
                            if 'scheduler' in self.modules: self.modules['scheduler'].apply_human_delay()
                        except Exception as e: self.report_issue("scheduler.py", str(e), "Fix timing logic")

                        # 3. ویڈیو اور اپلوڈ - Fail Safe
                        try:
                            if 'video_gen' in self.modules and 'uploader' in self.modules:
                                vid = self.modules['video_gen'].create_unique_video_metadata(account_id, country)
                                self.modules['uploader'].upload_video(account_id, vid)
                        except Exception as e: self.report_issue("uploader.py", str(e), "Check API/Proxy connection")

                        # 4. ہیلتھ چیک - Fail Safe
                        try:
                            if 'health' in self.modules and self.modules['health'].check_shop_eligibility(account_id):
                                stats["shop_eligible"] += 1
                                self.log(f"⭐ Eligible: {account_id}")
                        except Exception as e: self.report_issue("health_tracker.py", str(e), "Check API response format")

                    processed += 1
                    stats["progress"] = int((processed / total_target) * 100)
                    time.sleep(random.uniform(1, 3))

                except Exception as e:
                    self.log(f"🚨 Critical skip on account {i+1}: {str(e)}")
                    continue

        stats["current_action"] = "Workflow Completed"
        self.is_running = False

master_bot = SmartDiagnosticEngine()

# --- HTML DASHBOARD (with Error Alert Section) ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>TikTok Engine 4 - Diagnostic Dashboard</title>
    <style>
        body { background: #0f0f0f; color: #e0e0e0; font-family: sans-serif; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; }
        .card p { font-size: 28px; font-weight: bold; color: #00ffcc; }
        .error-section { background: #2a0000; border: 1px solid #ff0000; border-radius: 10px; padding: 15px; margin-bottom: 20px; color: #ffcccc; }
        .error-item { margin-bottom: 10px; font-family: monospace; border-bottom: 1px solid #440000; padding-bottom: 5px; }
        .progress-container { background: #222; border-radius: 20px; height: 25px; width: 100%; margin: 20px 0; position: relative; }
        .progress-bar { background: linear-gradient(90deg, #ff4b2b, #ff416c); height: 100%; border-radius: 20px; width: {{progress}}%; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 2px; font-size: 14px; }
        .log-box { background: #000; border: 1px solid #333; border-radius: 10px; padding: 15px; height: 250px; overflow-y: auto; font-family: monospace; color: #00ff00; }
        .btn { background: #00ffcc; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <span><strong style="color:#00ffcc;">سسٹم اسٹیٹس:</strong> {{current_action}}</span>
        <a href="/start" class="btn">انجن چلائیں 🚀</a>
    </div>

    {% if errors %}
    <div class="error-section">
        <h3 style="color:red; margin-top:0;">⚠️ سسٹم میں کمیاں (Diagnostic Report)</h3>
        {% for err in errors %}<div class="error-item">{{err}}</div>{% endfor %}
    </div>
    {% endif %}

    <div class="grid">
        <div class="card"><h3>کل اکاؤنٹس</h3><p>{{total}}</p></div>
        <div class="card"><h3>ایکٹو</h3><p>{{active}}</p></div>
        <div class="card"><h3>ناکام</h3><p>{{terminated}}</p></div>
        <div class="card"><h3>شاپ ایلیجیبل ✅</h3><p>{{eligible}}</p></div>
    </div>

    <div class="progress-container">
        <div class="progress-bar" style="width: {{progress}}%"></div>
        <div class="progress-text">مکمل: {{progress}}%</div>
    </div>

    <h3>لائیو لاگز (Execution Logs)</h3>
    <div class="log-box">{% for log in logs %}<div style="margin-bottom:5px;">{{log}}</div>{% endfor %}</div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(
        DASHBOARD_HTML, total=stats["total_accounts"], active=stats["active"], 
        terminated=stats["terminated"], eligible=stats["shop_eligible"], 
        progress=stats["progress"], current_action=stats["current_action"], 
        logs=stats["logs"], errors=stats["critical_errors"]
    )

@app.route('/start')
def start_engine():
    if not getattr(master_bot, 'is_running', False):
        config = {"UK": 10, "USA": 10} 
        threading.Thread(target=master_bot.run_safe_workflow, args=(config,)).start()
        return "انجن شروع ہو گیا ہے! ڈیش بورڈ دیکھیں تاکہ کمیاں معلوم ہو سکیں۔"
    return "انجن پہلے سے چل رہا ہے!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
