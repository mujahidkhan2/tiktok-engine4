import os
import subprocess
import logging
from datetime import datetime

class TheBrain:
    def __init__(self):
        self.SECRET_KEY = "OWNER_MASTER_KEY_2026"
        self.project_root = os.getcwd()
        self.version = "v3.0_Autonomous_GodMode"
        self.master_bot = None # This will be linked in app.py
        
        logging.basicConfig(filename='brain_activity.log', level=logging.INFO, 
                            format='%(asctime)s - BRAIN - %(message)s')

    def verify_owner(self, key):
        return key == self.SECRET_KEY

    def scan_project_structure(self):
        structure = {}
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                structure[file] = os.path.join(root, file)
        return structure

    def execute_system_command(self, command):
        try:
            logging.info(f"Executing: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

    def modify_file_content(self, filename, search_text, replace_text):
        try:
            files = self.scan_project_structure()
            if filename in files:
                filepath = files[filename]
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if search_text in content:
                    new_content = content.replace(search_text, replace_text)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return f"Success: {filename} updated."
                return "Error: Text not found."
            return "Error: File not found."
        except Exception as e:
            return f"Critical Error: {str(e)}"

    def restart_server(self):
        try:
            # Railway uses Procfile or main.py; triggering a restart
            self.execute_system_command("touch main.py") 
            return "Server restart triggered. System is rebooting..."
        except Exception as e:
            return f"Restart failed: {str(e)}"

    def self_evaluate(self):
        return f"Brain Version: {self.version} | Status: Autonomous | Power: 100%"

    def execute_command(self, text):
        text = text.lower()
        if "restart" in text:
            return self.restart_server()
        elif "status" in text or "evaluate" in text:
            return self.self_evaluate()
        elif "stop" in text or "kill" in text:
            if self.master_bot:
                self.master_bot.is_running = False
                return "Engine stopped by The Brain."
            return "Engine not found."
        elif "scan" in text:
            struct = self.scan_project_structure()
            return f"Project scanned. Found {len(struct)} files."
        else:
            return f"Command received: '{text}'. I am processing this within the matrix."

brain = TheBrain()