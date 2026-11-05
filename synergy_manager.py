from flask import Flask, render_template_string, request, redirect, url_for, flash
from engine import TikTokEngine
from synergy_manager import SynergyManager
from traffic_pipeline import TrafficPipeline
from health_tracker import HealthTracker
from identity_generator import IdentityGenerator
import threading
import re

app = Flask(__name__)
app.secret_key = "tiktok_vip_secret_key_2026"

# --- SMART COUNTRY LIST ---
# ان ممالک کے نام سسٹم خود پہچانے گا چاہے آپ کسی بھی فارمیٹ میں لکھیں
SUPPORTED_COUNTRIES = [
    "UK", "USA", "SAUDI", "UAE", "DUBAI", "PK", "PAKISTAN", 
    "IN", "INDIA", "BD", "BANGLADESH", "TURKEY", "FRANCE", "GERMANY"
]

try:
    engine = TikTokEngine()
    synergy = SynergyManager(engine) 
    traffic = TrafficPipeline(engine) 
    health = HealthTracker()
    id_gen = IdentityGenerator()
except Exception as e:
    print(f"❌ سسٹم شروع کرنے میں غلطی: {e}")

# HTML ٹیمپلیٹ (بلکل وہی ہے، بس ہنٹ میسج اپڈیٹ کیا ہے)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Engine 4 (Super-Admin Edition)</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #eee; text-align: right; margin: 0; padding: 0; }
        .header { background-color: #000; color: #fff; padding: 20px; text-align: center; border-bottom: 3px solid #fe2c55; }
        .container { padding: 20px; max-width: 1100px; margin: auto; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); margin-bottom: 20px; border: 1px solid #333; }
        
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; margin-bottom: 20px; }
        .stat-box { background: #252525; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #444; }
        .stat-box h4 { margin: 0; font-size: 14px; color: #aaa; }
        .stat-box p { margin: 5px 0 0; font-size: 22px; font-weight: bold; color: #fe2c55; }

        .admin-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e1e1e; color: white; direction: ltr; }
        .admin-table th, .admin-table td { padding: 12px; border: 1px solid #333; text-align: center; font-size: 14px; }
        .admin-table th { background: #333; color: #fe2c55; }
        .status-Active { color: #00ff00; }
        .status-Paused { color: #ffff00; }
        .status-Slow { color: #ffa500; }
        .status-Terminated { color: #ff0000; }

        .btn { display: inline-block; padding: 8px 12px; margin: 2px; border: none; border-radius: 5px; font-size: 12px; cursor: pointer; transition: 0.3s; text-align: center; text-decoration: none; font-weight: bold; color: white; }
        .btn-primary { background-color: #fe2c55; }
        .btn-secondary { background-color: #25d366; }
        .btn-danger { background-color: #ff4b2b; }
        .btn-info { background-color: #1da1f2; }
        .btn-play { background: green; }
        .btn-pause { background: orange; }
        .btn-slow { background: blue; }
        .btn-kill { background: red; }
        .btn-link { background: #555; }

        .alert { padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center; font-weight: bold; }
        .alert-success { background-color: #d4edda; color: #155724; }
        .alert-danger { background-color: #f8d7da; color: #721c24; }
        .status-box { background: #000; color: #00ff00; padding: 15px; border-radius: 10px; font-family: 'Courier New', monospace; direction: ltr; text-align: left; white-space: pre-wrap; }
        input[type="text"], input[type="number"] { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #444; border-radius: 8px; background: #252525; color: white; font-size: 16px; }
        .hint { font-size: 12px; color: #888; margin-bottom: 10px; display: block; }
    </style>
</head>
<body dir="rtl">
    <div class="header">
        <h1>🚀 TikTok Engine 4 (Super-Admin Edition)</h1>
        <p>اسٹیلتھ موڈ: فعال | میوچل گروتھ: آن | لائیو مانیٹرنگ: فعال</p>
    </div>
    <div class="container">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert {% if '✅' in message %}alert-success{% else %}alert-danger{% endif %}">
                {{ message }}
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <div class="stats-grid">
            <div class="stat-box"><h4>کل اکاؤنٹس</h4><p>{{ stats.total }}</p></div>
            <div class="stat-box"><h4>وارم اپ جاری ہے</h4><p>{{ stats.warming }}</p></div>
            <div class="stat-box"><h4>ویڈیوز اپلوڈڈ</h4><p>{{ stats.uploaded }}</p></div>
            <div class="stat-box"><h4>VIP سیل ایبل</h4><p>{{ stats.vip }}</p></div>
        </div>

        <div class="card">
            <h3>⚙️ ماسٹر کنٹرول پینل</h3>
            <form action="/action" method="post">
                <label>اکاؤنٹس کی تعداد یا لوکیشن مکس:</label>
                <input type="text" name="amount" placeholder="مثلاً: 100 یا UK 50 USA 30 PK 20">
                <span class="hint">اب آپ صرف 'UK 10' یا 'USA 20' لکھیں، کوئی کومہ یا کولن کی ضرورت نہیں۔ سسٹم خود پہچان لے گا۔</span>
                <button type="submit" name="task" value="create" class="btn btn-primary">📦 اکاؤنٹس جنریٹ کریں</button>
                
                <label>ٹریفک لنک (URL):</label>
                <input type="text" name="url" placeholder="https://tiktok.com/@user/video/...">
                <button type="submit" name="task" value="traffic" class="btn btn-secondary">🔗 ٹریفک پائپ لائن چلائیں</button>
                
                <button type="submit" name="task" value="boost" class="btn btn-info">📈 میوچل نیٹ ورک بوسٹ</button>
                <button type="submit" name="task" value="health" class="btn btn-info">📊 ویلیو اور ہیلتھ رپورٹ</button>
                <button type="submit" name="task" value="status" class="btn btn-info">🔍 سسٹم سٹیٹس</button>
                <button type="submit" name="task" value="clear" class="btn btn-danger" onclick="return confirm('ڈیٹا ڈیلیٹ کریں؟')">🗑️ ڈیٹا صاف کریں</button>
            </form>
        </div>

        <div class="card">
            <h3>👥 لائیو آرمی مانیٹر (Account Explorer)</h3>
            <div style="overflow-x:auto;">
                <table class="admin-table">
                    <tr>
                        <th>Username</th>
                        <th>Password</th>
                        <th>Country</th>
                        <th>Status</th>
                        <th>Profile / Video</th>
                        <th>Quick Control</th>
                    </tr>
                    {% for user, data in accounts.items() %}
                    <tr>
                        <td>{{ user }}</td>
                        <td>{{ data.password }}</td>
                        <td>{{ data.country }}</td>
                        <td class="status-{{ data.status }}">{{ data.status }}</td>
                        <td>
                            <a href="https://www.tiktok.com/@{{ user }}" target="_blank" class="btn btn-link">🌐 View Profile</a>
                        </td>
                        <td>
                            <a href="/update_status/{{ user }}/Active" class="btn btn-play">▶</a>
                            <a href="/update_status/{{ user }}/Paused" class="btn btn-pause">⏸</a>
                            <a href="/update_status/{{ user }}/Slow" class="btn btn-slow">🐢</a>
                            <a href="/update_status/{{ user }}/Terminated" class="btn btn-kill">💀</a>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </div>

        {% if report %}
        <div class="card">
            <h3>📋 رزلٹ / رپورٹ</h3>
            <div class="status-box">{{ report }}</div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def parse_hybrid_input(user_input):
    """
    ULTRA-FLEXIBLE PARSER:
    1. Recognizes countries from a predefined list regardless of symbols.
    2. Handles 'UK 10', 'UK:10', 'UK,10', '100' (simple number).
    3. No more crashes.
    """
    if not user_input:
        return None, None
        
    user_input = user_input.strip().upper()
    
    # Case 1: Simple number (e.g., "100")
    if user_input.isdigit():
        return int(user_input), None

    try:
        specs = {}
        # We split by common delimiters or spaces
        # This replaces commas, colons, and semicolons with spaces to simplify
        normalized_input = user_input.replace(',', ' ').replace(':', ' ').replace(';', ' ')
        tokens = normalized_input.split()

        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Check if this token is a supported country
            if token in SUPPORTED_COUNTRIES:
                # The next token should be the number
                if i + 1 < len(tokens):
                    try:
                        count = int(tokens[i+1])
                        specs[token] = count
                        i += 2 # Skip both country and number
                        continue
                    except ValueError:
                        # If the next token isn't a number, just move on
                        pass
            i += 1
        
        if not specs:
            # Final attempt: try to find any number in the string
            nums = re.findall(r'\d+', user_input)
            if nums:
                return int(nums[0]), None
            return None, None
            
        total_count = sum(specs.values())
        return total_count, specs
        
    except Exception as e:
        print(f"Critical Parsing Error: {e}")
        return None, None

@app.route('/')
def index():
    all_accs = engine.acc_manager.get_all_accounts()
    stats = {
        "total": len(all_accs),
        "warming": len([a for a in all_accs if a.get('status') == 'warming' or a.get('status') == 'Active']),
        "uploaded": len([a for a in all_accs if a.get('status') == 'uploaded']),
        "vip": len([a for a in all_accs if a.get('status') == 'vip'])
    }
    return render_template_string(HTML_TEMPLATE, stats=stats, accounts=all_accs)

@app.route('/update_status/<username>/<status>')
def update_status(username, status):
    try:
        engine.acc_manager.update_status(username, status)
        flash(f"✅ {username} کا اسٹیٹس {status} کر دیا گیا ہے۔")
    except Exception as e:
        flash(f"❌ غلطی: {e}")
    return redirect(url_for('index'))

@app.route('/action', methods=['POST'])
def action():
    task = request.form.get('task')
    amount_input = request.form.get('amount')
    url = request.form.get('url')
    report = None

    if task == 'create':
        if amount_input:
            try:
                # Use the new ultra-flexible parser
                count, specs = parse_hybrid_input(amount_input)
                
                if count is None:
                    # Instead of crashing, we give a very clear hint
                    flash("❌ ان پٹ سمجھ نہیں آیا! براہ کرم 'UK 10' یا '100' کی طرح لکھیں۔")
                    return redirect(url_for('index'))
                
                def run_creation():
                    try:
                        engine.create_batch_accounts(count, custom_specs=specs)
                    except Exception as inner_e:
                        print(f"Engine Execution Error: {inner_e}")
                
                threading.Thread(target=run_creation).start()
                flash(f"✅ {count} اکاؤنٹس کا عمل شروع ہو گیا ہے۔")
            except Exception as e:
                flash(f"❌ سسٹم ایرر: {e}")
        else:
            flash("❌ براہ کرم تعداد لکھیں!")

    elif task == 'boost':
        try:
            batches = synergy.coordinate_workers(total_accounts=1000)
            threading.Thread(target=synergy.run_growth_cycle, args=(batches,)).start()
            flash("✅ میوچل گروتھ سائیکل شروع ہو گیا ہے!")
        except Exception as e:
            flash(f"❌ غلطی: {e}")

    elif task == 'traffic':
        if url:
            try:
                all_accounts = engine.acc_manager.get_all_accounts()
                threading.Thread(target=traffic.route_traffic, args=(url, all_accounts, "main")).start()
                flash(f"✅ ٹریفک پائپ لائن فعال کر دی گئی ہے!")
            except Exception as e:
                flash(f"❌ غلطی: {e}")
        else:
            flash("❌ براہ کرم لنک درج کریں!")

    elif task == 'health':
        res = health.generate_detailed_report()
        report = f"--- 📊 NETWORK HEALTH REPORT ---\nTotal Accounts: {res['summary']['total']}\nHealthy: {res['summary']['healthy']}\n🌟 VIP Sellable: {res['summary']['vip_sellable']}"

    elif task == 'status':
        status = engine.get_system_status()
        report = f"System Status: {status['system_health']}\nTotal Managed Accounts: {status['total_accounts']}"

    elif task == 'clear':
        engine.acc_manager.clear_all_accounts()
        flash("🗑️ تمام ڈیٹا صاف کر دیا گیا!")

    return render_template_string(HTML_TEMPLATE, report=report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
