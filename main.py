import os
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, render_template_string, redirect, url_for, request, jsonify

# Import Brain and Engine Modules
try:
    from brain_core import brain
    from engine import TikTokEngine
except ImportError as e:
    print(f"Critical Import Error: {e}")

app = Flask(__name__)

# Global Stats
stats = {
    "total_accounts": 0, "active": 0, "paused": 0, "terminated": 0,
    "shop_eligible": 0, "current_action": "System Standby", 
    "logs": [], "critical_errors": [], "viral_accounts": [], "risk_accounts": []
}

class GhostMatrixEngine:
    def __init__(self):
        self.is_running = False
        try:
            self.engine = TikTokEngine()
            all_accs = self.engine.acc_manager.get_all_accounts()
            stats["total_accounts"] = len(all_accs)
        except Exception as e:
            self.log(f"Init Error: {e}", "ERROR")

    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARN": "⚠️", "ERROR": "🚨"}.get(level, "ℹ️")
        formatted_msg = f"[{timestamp}] {prefix} {message}"
        stats["logs"].insert(0, formatted_msg)
        if len(stats["logs"]) > 100: stats["logs"].pop()

    def run_parallel_workflow(self, config, target_url=None):
        self.is_running = True
        stats["current_action"] = "Executing Workflow..."
        
        all_tasks = []
        for country, count in config.items():
            for _ in range(count): all_tasks.append(country)

        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(lambda c: self.account_lifecycle(c, target_url), all_tasks)
        
        self.is_running = False
        stats["current_action"] = "Workflow Completed"

    def account_lifecycle(self, country, target_url):
        try:
            acc_id = self.engine.create_account(country)
            if not acc_id: return
            
            stats["total_accounts"] += 1
            stats["active"] += 1
            self.log(f"Account Active: {acc_id} ({country})", "SUCCESS")

            while self.is_running:
                if target_url:
                    behavior = random.choice(['full_support', 'casual_like', 'ghost_view'])
                    self.engine.execute_boost_action(acc_id, target_url, behavior)
                    time.sleep(random.randint(300, 900))
                else:
                    time.sleep(random.randint(600, 3600))
        except Exception as e:
            self.log(f"Lifecycle Error: {str(e)}", "ERROR")

# Initialize the main engine
master_bot = GhostMatrixEngine()

# CRITICAL LINK: Connect The Brain to the actual Engine Body
brain.master_bot = master_bot

# DASHBOARD HTML (Full Theme)
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
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>GHOST MATRIX v4</h2>
        <a href="/" class="nav-btn">🏠 مین کمانڈ سینٹر</a>
        <a href="/brain" class="nav-btn" style="color: var(--neon-purple);">🧠 THE BRAIN (منشی)</a>
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
            <h3>🚀 بوسٹنگ اور ریکروٹمنٹ</h3>
            <form action="/start" method="post" class="input-group">
                <input type="text" name="target_url" placeholder="Target URL" style="width: 300px;">
                UK: <input type="number" name="UK" value="0" style="width: 50px;"> 
                USA: <input type="number" name="USA" value="0" style="width: 50px;"> 
                PK: <input type="number" name="PK" value="0" style="width: 50px;"> 
                <button type="submit" class="btn btn-primary">لانچ کریں ⚡</button>
            </form>
        </div>
        <div class="log-container">
            {% for log in logs %} <div class="log-entry">{{ log }}</div> {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, total=stats["total_accounts"], active=stats["active"], eligible=stats["shop_eligible"], terminated=stats["terminated"], current_action=stats["current_action"], logs=stats["logs"])

@app.route('/start', methods=['POST'])
def start():
    target_url = request.form.get('target_url')
    config = {"UK": int(request.form.get('UK', 0)), "USA": int(request.form.get('USA', 0)), "PK": int(request.form.get('PK', 0))}
    threading.Thread(target=master_bot.run_parallel_workflow, args=(config, target_url)).start()
    return redirect(url_for('index'))

@app.route('/kill')
def kill():
    master_bot.is_running = False
    stats["current_action"] = "🛑 EMERGENCY STOP"
    return redirect(url_for('index'))

@app.route('/inventory')
def inventory():
    accs = master_bot.engine.acc_manager.get_all_accounts()
    html = "<h1 style='color:white;'>Account Inventory</h1><table border='1' style='color:white; background:black; width:100%'><tr><th>User</th><th>Country</th><th>Status</th></tr>"
    for u, d in accs.items(): html += f"<tr><td>{u}</td><td>{d['country']}</td><td>{d['status']}</td></tr>"
    html += "</table><br><a href='/' style='color:green;'>Back</a>"
    return htmlیہ رہا آپ کے `app.py` کا مکمل اور فائنل کوڈ۔ میں نے اس میں آپ کے **تمام پرانے فیچرز** (Inventory, Boosting Hub, Kill Switch, Stats) کو برقرار رکھا ہے اور صرف `The Brain` کی لنکنگ کو ٹھیک کیا ہے تاکہ وہ اب کریش نہ ہو اور آپ کی بلیک سکرین کا مسئلہ حل ہو جائے۔

اس کوڈ کو مکمل طور پر کاپی کر کے `app.py` میں پیسٹ کر دیں:

```python
import os
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render\_template, render\_template\_string, redirect, url\_for, request, jsonify

# Import Brain and Engine Modules
try:
    from brain\_core import brain
    from engine import TikTokEngine
except ImportError as e:
    print(f"Critical Import Error: {e}")

app = Flask(__name__)

# Global Stats
stats = {
    "total\_accounts": 0, "active": 0, "paused": 0, "terminated": 0,
    "shop\_eligible": 0, "current\_action": "System Standby", 
    "logs": [], "critical\_errors": [], "viral\_accounts": [], "risk\_accounts": []
}

class GhostMatrixEngine:
    def __init__(self):
        self.is\_running = False
        try:
            self.engine = TikTokEngine()
            all\_accs = self.engine.acc\_manager.get\_all\_accounts()
            stats["total\_accounts"] = len(all\_accs)
        except Exception as e:
            self.log(f"Init Error: {e}", "ERROR")

    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARN": "⚠️", "ERROR": "🚨"}.get(level, "ℹ️")
        formatted\_msg = f"[{timestamp}] {prefix} {message}"
        stats["logs"].insert(0, formatted\_msg)
        if len(stats["logs"]) > 100: stats["logs"].pop()

    def run\_parallel\_workflow(self, config, target\_url=None):
        self.is\_running = True
        stats["current\_action"] = "Executing Workflow..."
        
        all\_tasks = []
        for country, count in config.items():
            for _ in range(count): all\_tasks.append(country)

        with ThreadPoolExecutor(max\_workers=20) as executor:
            executor.map(lambda c: self.account\_lifecycle(c, target\_url), all\_tasks)
        
        self.is\_running = False
        stats["current\_action"] = "Workflow Completed"

    def account\_lifecycle(self, country, target\_url):
        try:
            acc\_id = self.engine.create\_account(country)
            if not acc\_id: return
            
            stats["total\_accounts"] += 1
            stats["active"] += 1
            self.log(f"Account Active: {acc\_id} ({country})", "SUCCESS")

            while self.is\_running:
                if target\_url:
                    behavior = random.choice(['full\_support', 'casual\_like', 'ghost\_view'])
                    self.engine.execute\_boost\_action(acc\_id, target\_url, behavior)
                    time.sleep(random.randint(300, 900))
                else:
                    time.sleep(random.randint(600, 3600))
        except Exception as e:
            self.log(f"Lifecycle Error: {str(e)}", "ERROR")

# Initialize the main engine
master\_bot = GhostMatrixEngine()

# CRITICAL LINK: Connecting The Brain to the Engine Body
brain.master\_bot = master\_bot

# DASHBOARD HTML (Full Theme maintained)
DASHBOARD\_HTML = """
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
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>GHOST MATRIX v4</h2>
        <a href="/" class="nav-btn">🏠 مین کمانڈ سینٹر</a>
        <a href="/brain" class="nav-btn" style="color: var(--neon-purple);">🧠 THE BRAIN (منشی)</a>
        <a href="/inventory" class="nav-btn">📦 اکاؤنٹ انوینٹری</a>
    </div>
    <div class="main-content">
        <div class="header">
            <div>
                <h1 style="margin:0; color:#fff;">Command Center <span style="font-size:16px; color:var(--neon-green);">v4.0 Stealth Engine</span></h1>
                <p style="margin:5px 0 0 0; color:#888;">سسٹم اسٹیٹس: <span class="status-pill">{{current\_action}}</span></p>
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
            <h3>🚀 بوسٹنگ اور ریکروٹمنٹ</h3>
            <form action="/start" method="post" class="input-group">
                <input type="text" name="target\_url" placeholder="Target URL" style="width: 300px;">
                UK: <input type="number" name="UK" value="0" style="width: 50px;"> 
                USA: <input type="number" name="USA" value="0" style="width: 50px;"> 
                PK: <input type="number" name="PK" value="0" style="width: 50px;"> 
                <button type="submit" class="btn btn-primary">لانچ کریں ⚡</button>
            </form>
        </div>
        <div class="log-container">
            {% for log in logs %} <div class="log-entry">{{ log }}</div> {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render\_template\_string(DASHBOARD\_HTML, total=stats["total\_accounts"], active=stats["active"], eligible=stats["shop\_eligible"], terminated=stats["terminated"], current\_action=stats["current\_action"], logs=stats["logs"])

@app.route('/start', methods=['POST'])
def start():
    target\_url = request.form.get('target\_url')
    config = {"UK": int(request.form.get('UK', 0)), "USA": int(request.form.get('USA', 0)), "PK": int(request.form.get('PK', 0))}
    threading.Thread(target=master\_bot.run\_parallel\_workflow, args=(config, target\_url)).start()
    return redirect(url\_for('index'))

@app.route('/kill')
def kill():
    master\_bot.is\_running = False
    stats["current\_action"] = "🛑 EMERGENCY STOP"
    return redirect(url\_for('index'))

@app.route('/inventory')
def inventory():
    try:
        accs = master\_bot.engine.acc\_manager.get\_all\_accounts()
        html = "<h1 style='color:white;'>Account Inventory</h1><table border='1' style='color:white; background:black; width:100%'><tr><th>User</th><th>Country</th><th>Status</th></tr>"
        for u, d in accs.items(): 
            html += f"<tr><td>{u}</td><td>{d.get('country','N/A')}</td><td>{d.get('status','N/A')}</td></tr>"
        html += "</table><br><a href='/' style='color:green;'>Back</a>"
        return html
    except Exception as e:
        return f"<h1 style='color:white;'>Error loading inventory: {e}</h1><a href='/' style='color:green;'>Back</a>"

@app.route('/brain')
def brain\_page():
    return render\_template('brain\_chat.html')

@app.route('/brain\_chat', methods=['POST'])
def brain\_chat():
    try:
        data = request.json
        user\_message = data.get('message', '')
        
        # Master Key Verification
        if brain.verify\_owner(user\_message):
            return jsonify({"response": "Master Key Verified. The Brain is now under your absolute control."})
        
        # Execute Command via Brain (Fixed: execute\_command now exists in brain\_core.py)
        response = brain.execute\_command(user\_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Brain Error: {str(e)}"}), 500

if __name__ == '\_\_main\_\_':
    # Bind to 0.0.0.0 and use port 8080 for Railway
    app.run(host='0.0.0.0', port=8080)
```_