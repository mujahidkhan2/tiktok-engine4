import os
import threading
import time
import random
from flask import Flask, render_template_string, redirect, url_for

# Import all modules
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

stats = {
    "total\_accounts": 0, "active": 0, "paused": 0, "terminated": 0,
    "shop\_eligible": 0, "progress": 0, "current\_action": "System Ready", 
    "logs": [], "critical\_errors": []
}

app = Flask(__name__)

class SmartDiagnosticEngine:
    def __init__(self):
        self.modules = {}
        self.load\_modules()
        self.guardian = SystemGuardian(self)

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        stats["logs"].insert(0, f"[{timestamp}] {message}")
        if len(stats["logs"]) > 25: stats["logs"].pop()

    def report\_issue(self, file\_name, error, solution):
        issue = f"❌ {file\_name} | {error} | Sol: {solution}"
        if issue not in stats["critical\_errors"]:
            stats["critical\_errors"].append(issue)
            self.log(f"🚨 ALERT: {file\_name} needs attention!")

    def load\_modules(self):
        try:
            engine = TikTokEngine()
            self.modules = {
                'engine': engine,
                'acc\_manager': engine.acc\_manager,
                'id\_gen': engine.id\_gen,
                'scheduler': Scheduler(),
                'video\_gen': VideoCreator(),
                'uploader': StealthUploader(engine),
                'health': HealthTracker(),
                'synergy': SynergyManager(engine),
                'traffic': TrafficPipeline(engine)
            }
            self.log("All modules loaded successfully.")
        except Exception as e:
            self.log(f"Module Load Failure: {e}")

    def run\_safe\_workflow(self, country\_config):
        self.is\_running = True
        total\_target = sum(country\_config.values())
        processed = 0

        for country, count in country\_config.items():
            for i in range(count):
                if not self.is\_running: break
                stats["current\_action"] = f"Processing {country} ({i+1}/{count})"
                
                try:
                    # 1. Account Creation
                    account\_id = self.modules['engine'].create\_account(country)
                    if account\_id:
                        stats["total\_accounts"] += 1
                        stats["active"] += 1
                        self.log(f"✅ Created: {account\_id}")
                        
                        # 2. Warming up
                        self.modules['scheduler'].human\_sleep\_pattern()

                        # 3. Content & Upload
                        vid = self.modules['video\_gen'].create\_unique\_video\_metadata(account\_id, country)
                        if self.modules['uploader'].upload\_video(account\_id, vid):
                            self.log(f"📤 Uploaded: {account\_id}")
                        else:
                            err = self.guardian.analyze\_account\_failure(account\_id, "Upload Failed")
                            self.report\_issue("uploader.py", err, "Check Proxy")

                        # 4. Health Check
                        if self.modules['health'].check\_shop\_eligibility(account\_id):
                            stats["shop\_eligible"] += 1
                            self.log(f"⭐ Shop Eligible: {account\_id}")

                    processed += 1
                    stats["progress"] = int((processed / total\_target) * 100)
                    time.sleep(random.uniform(1, 3))

                except Exception as e:
                    self.log(f"🚨 Critical Skip: {str(e)}")
                    continue

        stats["current\_action"] = "Workflow Completed"
        self.is\_running = False

master\_bot = SmartDiagnosticEngine()

DASHBOARD\_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>TikTok Engine 4 - Industrial Hub</title>
    <style>
        body { background: #0f0f0f; color: #e0e0e0; font-family: sans-serif; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; }
        .card p { font-size: 28px; font-weight: bold; color: #00ffcc; }
        .error-section { background: #2a0000; border: 1px solid #ff0000; border-radius: 10px; padding: 15px; margin-bottom: 20px; color: #ffcccc; }
        .progress-container { background: #222; border-radius: 20px; height: 25px; width: 100%; margin: 20px 0; position: relative; }
        .progress-bar { background: linear-gradient(90deg, #ff4b2b, #ff416c); height: 100%; border-radius: 20px; width: {{progress}}%; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 2px; font-size: 14px; }
        .log-box { background: #000; border: 1px solid #333; border-radius: 10px; padding: 15px; height: 250px; overflow-y: auto; font-family: monospace; color: #00ff00; }
        .btn { background: #00ffcc; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; text-decoration:none; }
        .nav-links { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="nav-links">
        <a href="/" class="btn">مین ڈیش بورڈ</a> | 
        <a href="/diagnostics" class="btn" style="background:#ffcc00;">انٹیلیجنس حب (مددگار) 🛠️</a>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <span><strong style="color:#00ffcc;">سسٹم اسٹیٹس:</strong> {{current\_action}}</span>
        <a href="/start" class="btn">انجن چلائیں 🚀</a>
    </div>

    {% if errors %}
    <div class="error-section">
        <h3 style="color:red; margin-top:0;">⚠️ سسٹم الرٹس</h3>
        {% for err in errors %<div style="margin-bottom:5px; font-family:monospace;">{{err}}</div>{% endfor %}
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

    <h3>لائیو لاگز</h3>
    <div class="log-box">{% for log in logs %<div style="margin-bottom:5px;">{{log}}</div>{% endfor %}</div>
</body>
</html>
"""

DIAGNOSTICS\_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Intelligence Hub - Diagnostics</title>
    <style>
        body { background: #0f0f0f; color: #e0e0e0; font-family: sans-serif; padding: 20px; }
        .card { background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #00ffcc; margin-bottom: 20px; }
        .btn { background: #00ffcc; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration:none; font-weight:bold; }
        .table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .table th, .table td { border: 1px solid #333; padding: 10px; text-align: right; }
        .eligible { color: #00ffcc; font-weight: bold; }
    </style>
</head>
<body>
    <a href="/" class="btn">واپس مین ڈیش بورڈ</a>
    <h1>🛠️ انٹیلیجنس حب (مددگار)</h1>
    
    <div class="card">
        <h3>💰 سیل ریڈی اکاؤنٹس (Shop Eligible)</h3>
        <table class="table">
            <tr><th>اکاؤنٹ</th><th>اسٹیٹس</th><th>ایکشن</th></tr>
            {% for user, data in accounts.items() if data.status == 'eligible' %}
            <tr>
                <td>{{user}}</td>
                <td class="eligible">Ready to Sell</td>
                <td><a href="/export/{{user}}" class="btn" style="padding:5px 10px; font-size:12px;">ڈیٹا نکالیں 📤</a></td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="card" style="border-color: #ff4444;">
        <h3>⚠️ سسٹم کی کمزوریاں اور مسائل</h3>
        {% for err in errors %<div style="color:#ffcccc; margin-bottom:10px; font-family:monospace;">{{err}}</div>{% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render\_template\_string(
        DASHBOARD\_HTML, total=stats["total\_accounts"], active=stats["active"], 
        terminated=stats["terminated"], eligible=stats["shop\_eligible"], 
        progress=stats["progress"], current\_action=stats["current\_action"], 
        logs=stats["logs"], errors=stats["critical\_errors"]
    )

@app.route('/diagnostics')
def diagnostics():
    return render\_template\_string(
        DIAGNOSTICS\_HTML, accounts=master\_bot.modules['acc\_manager'].get\_all\_accounts(), 
        errors=stats["critical\_errors"]
    )

@app.route('/export/<username>')
def export\_acc(username):
    data = master\_bot.modules['acc\_manager'].export\_account\_data(username)
    return f"<h1>Account Data for {username}</h1><pre>{json.dumps(data, indent=4)}</pre><br><a href='/diagnostics'>واپس جائیں</a>"

@app.route('/start')
def start\_engine():
    if not getattr(master\_bot, 'is\_running', False):
        config = {"USA": 5, "UK": 5} 
        threading.Thread(target=master\_bot.run\_safe\_workflow, args=(config,)).start()
        return redirect(url\_for('dashboard'))
    return redirect(url\_for('dashboard'))

if __name__ == '\_\_main\_\_':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
