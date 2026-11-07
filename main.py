import os
import threading
import time
import random
import json
from flask import Flask, render_template_string, redirect, url_for

# Import all stealth modules with safety wrapper
try:
    from account_manager import AccountManager
    from identity_generator import IdentityGenerator
    from engine import TikTokEngine
    from scheduler import Scheduler
    from video_creator import VideoCreator
    from uploader import StealthUploader
    from health_tracker import HealthTracker
    from synergy_manager import SynergyManager
    from traffic_pipeline import TrafficPipeline
    from system_guardian import SystemGuardian
except ImportError as e:
    print(f"Critical Import Error: {e}")

# Global System Stats - Industrial Grade Tracking
stats = {
    "total_accounts": 0, 
    "active": 0, 
    "paused": 0, 
    "terminated": 0,
    "shop_eligible": 0, 
    "progress": 0, 
    "current_action": "System Ready", 
    "logs": [], 
    "critical_errors": []
}

app = Flask(__name__)

class SmartDiagnosticEngine:
    def __init__(self):
        self.modules = {}
        self.is_running = False
        self.load_modules()
        try:
            self.guardian = SystemGuardian(self)
        except Exception as e:
            self.log(f"Guardian Init Error: {e}")

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"
        stats["logs"].insert(0, formatted_msg)
        if len(stats["logs"]) > 50: 
            stats["logs"].pop()

    def report_issue(self, file_name, error, solution):
        issue = f"❌ {file_name} | {error} | Sol: {solution}"
        if issue not in stats["critical_errors"]:
            stats["critical_errors"].append(issue)
            self.log(f"🚨 ALERT: {file_name} needs attention!")

    def load_modules(self):
        try:
            engine = TikTokEngine()
            self.modules = {
                'engine': engine,
                'acc_manager': engine.acc_manager,
                'id_gen': engine.id_gen,
                'scheduler': Scheduler(),
                'video_gen': VideoCreator(),
                'uploader': StealthUploader(engine),
                'health': HealthTracker(),
                'synergy': SynergyManager(engine),
                'traffic': TrafficPipeline(engine)
            }
            self.log("🚀 All stealth modules initialized successfully.")
        except Exception as e:
            self.log(f"⚠️ Module Load Failure: {e}")
            self.report_issue("System Initialization", str(e), "Check requirements.txt")

    def run_safe_workflow(self, country_config):
        self.is_running = True
        total_target = sum(country_config.values())
        processed = 0

        self.log("⚡ Starting Industrial Stealth Workflow...")
        
        for country, count in country_config.items():
            for i in range(count):
                if not self.is_running: 
                    break
                
                stats["current_action"] = f"Processing {country} ({i+1}/{count})"
                
                try:
                    account_id = self.modules['engine'].create_account(country)
                    if account_id:
                        stats["total_accounts"] += 1
                        stats["active"] += 1
                        self.log(f"✅ Account Created: {account_id} ({country})")
                        
                        self.modules['scheduler'].human_sleep_pattern()

                        vid_meta = self.modules['video_gen'].create_unique_video_metadata(account_id, country)
                        if self.modules['uploader'].upload_video(account_id, vid_meta):
                            self.log(f"📤 Stealth Upload Success: {account_id}")
                        else:
                            err = self.guardian.analyze_account_failure(account_id, "Upload Failed")
                            self.report_issue("uploader.py", err, "Rotate Residential Proxies")

                        if self.modules['health'].check_shop_eligibility(account_id):
                            stats["shop_eligible"] += 1
                            self.log(f"⭐ Shop Eligible: {account_id} is ready!")

                    processed += 1
                    stats["progress"] = int((processed / total_target) * 100)
                    time.sleep(random.uniform(2, 5))

                except Exception as e:
                    self.log(f"🚨 Workflow Skip: {str(e)}")
                    self.report_issue("Workflow Engine", str(e), "Review engine.py")
                    continue

        stats["current_action"] = "Workflow Completed Successfully"
        self.is_running = False
        self.log("🏁 All targets processed.")

master_bot = SmartDiagnosticEngine()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>TikTok Engine 4 - Industrial Hub</title>
    <style>
        body { background: #0a0a0a; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; padding: 30px; }
        .nav-links { margin-bottom: 30px; display: flex; gap: 15px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: #161616; padding: 25px; border-radius: 20px; border: 1px solid #333; text-align: center; }
        .card p { font-size: 32px; font-weight: bold; color: #00ffcc; margin: 10px 0 0 0; }
        .error-section { background: #2a0000; border: 1px solid #ff0000; border-radius: 15px; padding: 20px; margin-bottom: 30px; color: #ffcccc; }
        .progress-container { background: #222; border-radius: 25px; height: 30px; width: 100%; margin: 25px 0; position: relative; border: 1px solid #444; overflow: hidden; }
        .progress-bar { background: linear-gradient(90deg, #ff4b2b, #ff416c); height: 100%; width: {{progress}}%; transition: width 0.5s ease-in-out; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 5px; font-size: 14px; font-weight: bold; color: white; }
        .log-box { background: #000; border: 1px solid #333; border-radius: 15px; padding: 20px; height: 300px; overflow-y: auto; font-family: 'Consolas', monospace; color: #00ff00; }
        .btn { background: #00ffcc; color: #000; padding: 12px 25px; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; text-decoration:none; display: inline-block; }
        .btn-warn { background: #ffcc00; }
    </style>
</head>
<body>
    <div class="nav-links">
        <a href="/" class="btn">مین ڈیش بورڈ</a>
        <a href="/diagnostics" class="btn btn-warn">انٹیلیجنس حب (مددگار) 🛠️</a>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:30px;">
        <div>
            <h1 style="margin:0; color:#fff;">TikTok Engine 4 <span style="font-size:14px; color:#00ffcc; vertical-align:middle;">v4.0 Stealth</span></h1>
            <p style="margin:5px 0 0 0; color:#888;">سسٹم اسٹیٹس: <strong style="color:#00ffcc;">{{current_action}}</strong></p>
        </div>
        <a href="/start" class="btn" style="font-size:18px;">انجن چلائیں 🚀</a>
    </div>
    {% if errors %}
    <div class="error-section">
        <h3 style="color:red; margin-top:0;">⚠️ سسٹم الرٹس (Critical Issues)</h3>
        {% for err in errors %}
        <div style="margin-bottom:8px; font-family:monospace; border-bottom:1px solid #4a0000; padding-bottom:5px;">{{err}}</div>
        {% endfor %}
    </div>
    {% endif %}
    <div class="grid">
        <div class="card"><h3>کل اکاؤنٹس</h3><p>{{total}}</p></div>
        <div class="card"><h3>ایکٹو</h3><p>{{active}}</p></div>
        <div class="card"><h3>ناکام/بلاک</h3><p>{{terminated}}</p></div>
        <div class="card"><h3>شاپ ایلیجیبل ✅</h3><p>{{eligible}}</p></div>
    </div>
    <div class="progress-container">
        <div class="progress-bar" style="width: {{progress}}%;"></div>
        <div class="progress-text">پروجیکٹ کی تکمیل: {{progress}}%</div>
    </div>
    <h3 style="color:#fff; margin-bottom:15px;">لائیو سسٹم لاگز (Industrial Stream)</h3>
    <div class="log-box">
        {% for log in logs %}
        <div style="margin-bottom:6px; border-left: 3px solid #00ffcc; padding-left:10px;">{{log}}</div>
        {% endfor %}
    </div>
</body>
</html>
"""

DIAGNOSTICS_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Intelligence Hub - Diagnostics</title>
    <style>
        body { background: #0a0a0a; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; padding: 30px; }
        .card { background: #161616; padding: 25px; border-radius: 20px; border: 1px solid #00ffcc; margin-bottom: 30px; box-shadow: 0 0 20px rgba(0,255,204,0.1); }
        .btn { background: #00ffcc; color: #000; padding: 12px 25px; border: none; border-radius: 10px; cursor: pointer; text-decoration:none; font-weight:bold; display: inline-block; }
        .table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #111; }
        .table th, .table td { border: 1px solid #333; padding: 15px; text-align: right; }
        .table th { background: #222; color: #00ffcc; }
        .eligible { color: #00ffcc; font-weight: bold; }
    </style>
</head>
<body>
    <a href="/" class="btn">واپس مین ڈیش بورڈ</a>
    <h1 style="margin-top:20px; color:#fff;">🛠️ انٹیلیجنس حب (Diagnostic Center)</h1>
    <div class="card">
        <h3 style="color:#00ffcc;">💰 مونیٹائزیشن ریڈی اکاؤنٹس (Shop Eligible)</h3>
        <table class="table">
            <thead>
                <tr><th>اکاؤنٹ ID</th><th>اسٹیٹس</th><th>ایکشن</th></tr>
            </thead>
            <tbody>
                {% for user, data in accounts.items() if data.status == 'eligible' %}
                <tr>
                    <td>{{user}}</td>
                    <td class="eligible">Ready for Shop</td>
                    <td><a href="/export/{{user}}" class="btn" style="padding:5px 15px; font-size:12px;">ڈیٹا ایکسپورٹ 📤</a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <div class="card" style="border-color: #ff4444;">
        <h3 style="color:#ff4444;">⚠️ سسٹم کی کمزوریاں اور حل</h3>
        {% for err in errors %}
        <div style="color:#ffcccc; margin-bottom:12px; font-family:monospace; background:#2a0000; padding:10px; border-radius:5px;">{{err}}</div>
        {% endfor %}
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
        logs=stats["logs"], 
        errors=stats["critical_errors"]
    )

@app.route('/diagnostics')
def diagnostics():
    accounts_data = {}
    if 'acc_manager' in master_bot.modules:
        accounts_data = master_bot.modules['acc_manager'].get_all_accounts()
    return render_template_string(DIAGNOSTICS_HTML, accounts=accounts_data, errors=stats["critical_errors"])

@app.route('/export/<username>')
def export_acc(username):
    try:
        data = master_bot.modules['acc_manager'].export_account_data(username)
        return f"<body style='background:#0a0a0a; color:#00ffcc; font-family:monospace; padding:40px;'><h1>Account Data for: {username}</h1><pre style='background:#111; padding:20px; color:white;'>{json.dumps(data, indent=4)}</pre><br><a href='/diagnostics' style='color:white;'>واپس جائیں</a></body>"
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/start')
def start_engine():
    if not getattr(master_bot, 'is_running', False):
        config = {"USA": 5, "UK": 5, "Germany": 5} 
        threading.Thread(target=master_bot.run_safe_workflow, args=(config,)).start()
        master_bot.log("🚀 Workflow Thread started...")
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
