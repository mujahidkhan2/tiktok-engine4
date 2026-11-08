import os
import threading
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template_string, render_template, redirect, url_for, request, jsonify

# ==============================================================================
# MODULES IMPORT
# ==============================================================================
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
    # New Brain Modules
    from brain_core import brain
    from brain_security import security_shield
except ImportError as e:
    print(f"Critical Import Error: {e}")

# ==============================================================================
# GLOBAL SYSTEM STATISTICS
# ==============================================================================
stats = {
    "total_accounts": 0, "active": 0, "paused": 0, "terminated": 0,
    "shop_eligible": 0, "current_action": "System Standby", 
    "logs": [], "critical_errors": [], "viral_accounts": [], "risk_accounts": []
}

app = Flask(__name__)

# ==============================================================================
# GHOST MATRIX CORE ENGINE
# ==============================================================================
class GhostMatrixEngine:
    def __init__(self):
        self.is_running = False
        self.load_modules()
        try:
            self.guardian = SystemGuardian(self)
        except Exception as e:
            self.log(f"Guardian Init Error: {e}", "ERROR")

    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARN": "⚠️", "ERROR": "🚨"}.get(level, "ℹ️")
        formatted_msg = f"[{timestamp}] {prefix} {message}"
        stats["logs"].insert(0, formatted_msg)
        if len(stats["logs"]) > 100: stats["logs"].pop()

    def load_modules(self):
        try:
            engine = TikTokEngine()
            self.modules = {
                'engine': engine, 'acc_manager': engine.acc_manager,
                'id_gen': engine.id_gen, 'scheduler': Scheduler(),
                'video_gen': VideoCreator(), 'uploader': StealthUploader(engine),
                'health': HealthTracker(), 'synergy': SynergyManager(engine),
                'traffic': TrafficPipeline(engine)
            }
            all_accs = self.modules['acc_manager'].get_all_accounts()
            stats["total_accounts"] = len(all_accs)
            self.log(f"🚀 System Restored: {len(all_accs)} accounts loaded from DB.", "SUCCESS")
        except Exception as e:
            self.log(f"Module Load Failure: {e}", "ERROR")

    def account_lifecycle(self, country, target_url=None):
        try:
            time.sleep(random.randint(1, 300))
            acc_id = self.modules['engine'].create_account(country)
            if not acc_id: return

            stats["total_accounts"] += 1
            stats["active"] += 1
            self.log(f"Account Active: {acc_id} ({country})", "SUCCESS")

            while self.is_running:
                if target_url:
                    behavior = random.choice(['full_support', 'casual_like', 'ghost_view'])
                    self.log(f"{acc_id} performing {behavior} on target", "INFO")
                    self.modules['engine'].execute_boost_action(acc_id, target_url, behavior)
                    time.sleep(random.randint(60, 600))
                else:
                    action = random.choice(['scroll', 'like', 'comment', 'upload', 'sleep'])
                    time.sleep(random.randint(10, 600))
                    if action == 'upload':
                        vid_meta = self.modules['video_gen'].create_unique_video_metadata(acc_id, country)
                        self.modules['uploader'].upload_video(acc_id, vid_meta)
                    elif action == 'sleep':
                        time.sleep(random.randint(1800, 14400))
        except Exception as e:
            self.log(f"Lifecycle Error: {str(e)}", "ERROR")

    def run_parallel_workflow(self, country_config, target_url=None):
        self.is_// running = True
        all_tasks = []
        for country, count in country_config.items():
            for _ in range(count): all_tasks.append(country)

        stats["current_action"] = f"Executing {len(all_tasks)} Accounts Workflow"
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(lambda c: self.account_lifecycle(c, target_url), all_tasks)
        self.is_running = False
        stats["current_action"] = "Workflow Completed"

master_bot = GhostMatrixEngine()

# ==============================================================================
# DASHBOARD HTML
# ==============================================================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>GHOST MATRIX v4 | Command Center</title>
    <style>
        :root { --neon-green: #00ffcc; --neon-red: #ff4444; --neon-purple: #8a2be2; --dark-bg: #0a0a0a; --card-bg: #161616; }
        body { background: var(--dark-bg); color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; }
        .sidebar { width: 260px; background: #000; height: 100vh; border-left: 1px solid #333; position: fixed; right: 0; top: 0; padding: 20px; box-sizing: border-box; }
        .sidebar h2 { color: var(--neon-green); text-align: center; border-bottom: 1px solid #333; padding-bottom: 15px; }
        .nav-btn { display: block; width: 100%; padding: 12px; margin-bottom: 10px; background: #111; border: 1px solid #333; color: #ccc; text-align: right; border-radius: 8px; cursor: pointer; text-decoration: none; transition: 0.3s; }
        .nav-btn:hover { background: var(--neon-green); color: #000; }
        .main-content { margin-right: 260px; padding: 30px; width: calc(100% - 260px); }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .status-pill { background: #222; padding: 5px 15px; border-radius: 20px; border: 1px solid var(--neon-green); color: var(--neon-green); }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: var(--card-bg); padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; transition: 0.3s; }
        .card:hover { border-color: var(--neon-green); }
        .card p { font-size: 32px; font-weight: bold; color: var(--neon-green); margin: 10px 0 0 0; }
        .panel { background: var(--card-bg); padding: 25px; border-radius: 20px; border: 1px solid #444; margin-bottom: 30px; }
        .input-group { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
        input { background: #222; border: 1px solid #444; color: #fff; padding: 10px; border-radius: 8px; }
        .log-container { background: #000; border: 1px solid #333; border-radius: 15px; padding: 20px; height: 300px; overflow-y: auto; font-family: monospace; }
        .btn { padding: 12px 25px; border-radius: 8px; border: none; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .btn-primary { background: var(--neon-green); color: #000; }
        .btn-danger { background: var(--neon-red); color: #fff; }
        .btn-brain { background: var(--neon-purple); color: #fff; box-shadow: 0 0 10px var(--neon-purple); }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>GHOST MATRIX v4</h2>
        <a href="/" class="nav-btn">🏠 مین کمانڈ سینٹر</a>
        <a href="/brain" class="nav-btn" style="color: var(--neon-purple);">🧠 THE BRAIN (منشی)</a>
        <a href="/health" class="nav-btn">🏥 ہیلتھ ٹریکر</a>
        <a href="/viral" class="nav-btn">🚀 ویریل لسٹ</a>
        <a href="/shop" class="nav-btn">🛒 شاپ ہب</a>
        <a href="/inventory" class="nav-btn">📦 اکاؤنٹ انوینٹری</a>
    </div>
    <div class="main-content">
        <div class="header">
            <div>
                <h1 style="margin:0; color:#fff;">Command Center <span style="font-size:16px; color:var(--neon-green);">v4.0 Stealth Engine</span></h1>
                <p style="margin:5px 0 0 0; color:#888;">سسٹم اسٹیٹس: <span class="status-pill">{{current_action}}</span></p>
            </div>
            <a href="/kill" class="btn btn-danger">EMERGENCY KILL 🛑</a>
        </div>
        <div class="grid">
            <div class="card"><h3>کل اکاؤنٹس</h3><p>{{total}}</p></div>
            <div class="card"><h3>ایکٹو</h3><p>{{active}}</p></div>
            <div class="card"><h3>شاپ اہل</h3><p>{{eligible}}</p></div>
            <div class="card"><h3>ٹرمینیٹڈ</h3><p>{{terminated}}</p></div>
        </div>
        <div class="panel">
            <h3>🚀 بوسٹنگ اور ریکروٹمنٹ (Targeted Engine)</h3>
            <form action="/start" method="post" class="input-group">
                <input type="text" name="target_url" placeholder="Target URL (For Boosting)" style="width: 350px;">
                UK: <input type="number" name="UK" value="0" style="width: 60px;"> 
                USA: <input type="number" name="USA" value="0" style="width: 60px;"> 
                PK: <input type="number" name="PK" value="0" style="width: 60px;"> 
                Custom: <input type="text" name="OtherCountry" placeholder="Code" style="width: 70px;">
                <input type="number" name="OtherCount" placeholder="Qty" style="width: 60px;">
                <button type="submit" class="btn btn-primary">پروجیکٹ لانچ کریں ⚡</button>
            </form>
        </div>
        <div class="log-container">
            {% for log in logs %} <div class="log-entry">{{ log }}</div> {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# ==============================================================================
# ROUTES
# ==============================================================================

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, total=stats["total_accounts"], active=stats["active"], eligible=stats["shop_eligible"], terminated=stats["terminated"], current_action=stats["current_action"], logs=stats["logs"])

@app.route('/start', methods=['POST'])
def start():
    target_url = request.form.get('target_url')
    config = {"UK": int(request.form.get('UK', 0)), "USA": int(request.form.get('USA', 0)), "PK": int(request.form.get('PK', 0))}
    other_country = request.form.get('OtherCountry')
    other_count = int(request.form.get('OtherCount', 0))
    if other_country and other_count > 0: config[other_country] = other_count
    
    threading.Thread(target=master_bot.run_parallel_workflow, args=(config, target_url)).start()
    return redirect(url_for('index'))

@app.route('/kill')
def kill():
    master_bot.is_running = False
    stats["current_action"] = "🛑 EMERGENCY STOP"
    return redirect(url_for('index'))

@app.route('/inventory')
def inventory():
    accs = master_bot.modules['acc_manager'].get_all_accounts()
    html = "<h1 style='color:white;'>Account Inventory</h1><table border='1' style='color:white; background:black; width:100%'><tr><th>User</th><th>Country</th><th>Status</th></tr>"
    for u, d in accs.items(): html += f"<tr><td>{u}</td><td>{d['country']}</td><td>{d['status']}</td></tr>"
    html += "</table><br><a href='/' style='color:green;'>Back</a>"
    return html

# --- THE BRAIN ROUTES ---
@app.route('/brain')
def brain_page():
    return render_template('brain_chat.html')

@app.route('/brain/execute', methods=['POST'])
def brain_execute():
    data = request.json
    user_key = data.get('key')
    command = data.get('command')
    
    # Security Check via brain_security.py
    if not security_shield.verify_token("owner", user_key):
        return jsonify({"status": "error", "response": "Access Denied: Invalid Security Token!"})
    
    # Command processing via brain_core.py
    response = brain.process_owner_command(user_key, command)
    return jsonify({"status": "success", "response": response})

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)