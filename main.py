import os
import threading
import time
import random
import json
from flask import Flask, render_template_string, redirect, url_for, request

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

stats = {
    "total_accounts": 0, "active": 0, "paused": 0, "terminated": 0,
    "shop_eligible": 0, "progress": 0, "current_action": "System Ready", 
    "logs": [], "critical_errors": []
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
        if len(stats["logs"]) > 50: stats["logs"].pop()

    def report_issue(self, file_name, error, solution):
        issue = f"❌ {file_name} | {error} | Sol: {solution}"
        if issue not in stats["critical_errors"]:
            stats["critical_errors"].append(issue)
            self.log(f"🚨 SENTRY ALERT: {file_name} needs attention!")

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
            self.log("🚀 Stealth Modules Initialized Successfully.")
        except Exception as e:
            self.log(f"⚠️ Module Load Failure: {e}")

    def run_safe_workflow(self, country_config):
        self.is_running = True
        total_target = sum(country_config.values())
        processed = 0

        self.log("⚡ Starting Chaotic Human Workflow...")
        
        for country, count in country_config.items():
            for i in range(count):
                if not self.is_running: break
                
                stats["current_action"] = f"Processing {country} ({i+1}/{count})"
                try:
                    account_id = self.modules['engine'].create_account(country)
                    if account_id:
                        stats["total_accounts"] += 1
                        stats["active"] += 1
                        self.log(f"✅ Account Created: {account_id} ({country})")
                        
                        # Human-like behavior: not every account does everything at once
                        self.modules['scheduler'].human_sleep_pattern()

                        if random.random() > 0.2: # 80% chance to upload immediately
                            vid_meta = self.modules['video_gen'].create_unique_video_metadata(account_id, country)
                            if self.modules['uploader'].upload_video(account_id, vid_meta):
                                self.log(f"📤 Stealth Upload Success: {account_id}")

                        if self.modules['health'].check_shop_eligibility(account_id):
                            stats["shop_eligible"] += 1
                            self.log(f"⭐ Shop Eligible: {account_id} is ready!")

                    processed += 1
                    stats["progress"] = int((processed / total_target) * 100)
                except Exception as e:
                    self.log(f"🚨 Workflow Skip: {str(e)}")
                    continue

        stats["current_action"] = "Workflow Completed Successfully"
        self.is_running = False

master_bot = SmartDiagnosticEngine()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>TikTok Engine 4 - Command Center</title>
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
        .btn-danger { background: #ff4444; color: white; }
        .config-panel { background: #1a1a1a; padding: 20px; border-radius: 20px; margin-bottom: 30px; border: 1px solid #444; }
        input { background: #222; color: white; border: 1px solid #444; padding: 10px; border-radius: 5px; margin: 5px; }
    </style>
</head>
<body>
    <div class="nav-links">
        <a href="/" class="btn">مین ڈیش بورڈ</a>
        <a href="/diagnostics" class="btn" style="background:#ffcc00;">انٹیلیجنس حب 🛠️</a>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:30px;">
        <div>
            <h1 style="margin:0; color:#fff;">TikTok Engine 4 <span style="font-size:14px; color:#00ffcc; vertical-align:middle;">v4.0 Command Center</span></h1>
            <p style="margin:5px 0 0 0; color:#888;">سسٹم اسٹیٹس: <strong style="color:#00ffcc;">{{current_action}}</strong></p>
        </div>
        <a href="/kill" class="btn btn-danger" style="font-size:18px;">Kill Switch 🛑</a>
    </div>
    
    <div class="config-panel">
        <h3 style="margin-top:0;">🚀 فوج کی بھرتی (Recruitment Center)</h3>
        <form action="/start" method="post">
            UK: <input type="number" name="UK" value="0"> 
            USA: <input type="number" name="USA" value="0"> 
            PK: <input type="number" name="PK" value="0"> 
            Other: <input type="text" name="OtherCountry" placeholder
