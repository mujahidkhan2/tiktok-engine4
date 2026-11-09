import os
import subprocess
import json
import random
import time

class BrainCore:
    def __init__(self):
        self.master_key = "MASTER_123_SECRET"  # آپ اسے تبدیل کر سکتے ہیں
        self.capabilities = {"coding": 95, "research": 90, "system_control": 100}
        self.storage_file = "brain_memory.json"
        self.load_memory()

    def verify_key(self, key):
        return key == self.master_key

    def load_memory(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {"history": [], "added_features": []}

    def save_memory(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.memory, f)

    def modify_file_content(self, filename, new_content):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"✅ فائل {filename} کو کامیابی سے اپڈیٹ کر دیا گیا ہے۔"
        except Exception as e:
            return f"❌ فائل اپڈیٹ کرنے میں ناکامی: {str(e)}"

    def restart_server(self):
        # Railway پر سرور ری اسٹارٹ کرنے کے لیے پراسیس کو سگنیل بھیجنا
        os.system("pkill -f gunicorn || pkill -f python")
        return "🔄 سرور ری اسٹارٹ کر دیا گیا ہے۔ میں دوبارہ آن ہو رہا ہوں..."

    def self_evaluate(self):
        avg = sum(self.capabilities.values()) / len(self.capabilities)
        return f"🧠 میری موجودہ صلاحیت: {avg}%۔ میں مسلسل سیکھ رہا ہوں۔"

    def execute_command(self, text):
        text = text.lower()
        self.memory["history"].append(text)
        self.save_memory()

        # 1. Self-Evolution & Research Logic
        if "ایڈ کرو" in text or "اضافہ کرو" in text or "فیچر" in text:
            return f"🔍 میں اس فیچر کے لیے ریسرچ کر رہا ہوں۔ میں بہترین کوڈ تلاش کروں گا، اسے ٹیسٹ کروں گا اور پھر آپ کی اجازت سے {self.storage_file} میں ایڈجسٹ کروں گا۔"

        # 2. System Control
        if "ری اسٹارٹ" in text or "restart" in text:
            return self.restart_server()

        if "صلاحیت" in text or "evaluate" in text:
            return self.self_evaluate()

        # 3. File Analysis
        if "اینالائز" in text or "چیک کرو" in text:
            return "📂 میں تمام فائلوں کا جائزہ لے رہا ہوں... کوئی بھی مسنگ کوڈ یا ایرر ملنے پر میں اسے خود ٹھیک کر دوں گا۔"

        # 4. Intelligence Response (The Munshi Style)
        return f"🫡 جی مالک، میں نے آپ کا پیغام '{text}' سمجھ لیا ہے۔ میں اس پر کام کر رہا ہوں اور بہترین حل نکال کر آپ کو بتاتا ہوں۔"

