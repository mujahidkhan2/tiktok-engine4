import os
import subprocess
import logging
from datetime import datetime

class TheBrain:
    def __init__(self):
        self.SECRET_KEY = "OWNER_MASTER_KEY_2026" 
        self.project_root = os.getcwd()
        self.version = "v2.0_Evolution"
        
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
            logging.info(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            logging.error(f"Command failed: {str(e)}")
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
                    logging.info(f"Successfully modified {filename}")
                    return f"Success: {filename} updated."
                else:
                    return "Error: Search text not found in file."
            else:
                return "Error: File not found in project structure."
        except Exception as e:
            logging.error(f"Modification error: {str(e)}")
            return f"Critical Error: {str(e)}"

    def restart_server(self):
        # Railway/Gunicorn automatically restarts on file change, 
        # but we trigger a touch on the main file to ensure it.
        try:
            self.execute_system_command("touch main.py")
            return "Server restart triggered successfully."
        except Exception as e:
            return f"Restart failed: {str(e)}"

    def self_evaluate(self):
        # Self-awareness logic: comparing current version vs ideal
        capabilities = {
            "file_system": 100,
            "code_execution": 95,
            "autonomous_evolution": 80,
            "security_control": 100
        }
        avg_score = sum(capabilities.values()) / len(capabilities)
        return f"Current Brain Version: {self.version} | Capability Score: {avg_score}%"

# Initialize the brain instance
brain = TheBrain()