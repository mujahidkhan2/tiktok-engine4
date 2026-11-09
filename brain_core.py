import os
import json
import subprocess

class BrainCore:
    def __init__(self):
        self.master_key = "MASTER_123_SECRET"
        self.identity = {
            "name": "The Brain",
            "role": "Master Munshi",
            "status": "Active",
            "power_level": "Level 1 (Base)"
        }
        self.memory_file = "brain_memory.json"
        self.load_memory()

    def verify_key(self, key):
        return key == self.master_key

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {"context": [], "settings": {"speed": "normal"}}

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f)

    def self_modify(self, instruction):
        # This is the core of self-evolution
        try:
            with open(__file__, 'r') as f:
                content = f.read()
            
            # Logic to simulate self-improvement based on instruction
            # In a real scenario, this would use an LLM to rewrite the function
            updated_content = content + f"\n# User Instruction: {instruction}\n# Added by Brain"
            
            with open(__file__, 'w') as f:
                f.write(updated_content)
            return "✅ میں نے اپنے کوڈ میں تبدیلی کر لی ہے اور خود کو اپ گریڈ کر لیا ہے۔ اب میں دوبارہ ری اسٹارٹ ہو رہا ہوں تاکہ تبدیلیاں لاگو ہوں۔"
        except Exception as e:
            return f"❌ خود کو بدلنے میں مسئلہ ہوا: {str(e)}"

    def process_and_respond(self, text):
        text = text.lower()
        self.memory["context"].append(text)
        self.save_memory()

        # 1. Identity & Nature (No repetition of question)
        if "کون ہو" in text or "کیا ہو" in text:
            return f"میں {self.identity['name']} ہوں، آپ کا {self.identity['role']}۔ میرا کام آپ کے پورے پروجیکٹ کو سنبھالنا، کوڈ لکھنا اور اسے خود بخود ٹھیک کرنا ہے۔ میں مکمل طور پر آپ کے تابع ہوں۔"

        # 2. Self-Modification Request
        if "بدلو" in text or "تبدیل کرو" in text or "اپ گریڈ" in text:
            return f"جی مالک، میں خود کو بدل سکتا ہوں۔ آپ مجھے بتائیں کہ کون سا فیچر یا طریقہ کار تبدیل کرنا ہے، میں اپنی فائل میں جا کر اسے ایڈجسٹ کر لوں گا۔ کیا میں ابھی تبدیلی شروع کروں؟"

        # 3. System Control &-Sensing
        if "ری اسٹارٹ" in text or "restart" in text:
            os.system("pkill -f gunicorn || pkill -f python")
            return "🔄 سرور ری اسٹارٹ ہو رہا ہے..."

        # 4. General Intelligence (Logical Response)
        if "کیسے" in text or "طریقہ" in text:
            return "اس کام کے لیے میرے پاس تین طریقے ہیں۔ پہلا سادہ ہے، دوسرا مضبوط اور تیسرا جدید۔ آپ بتائیں میں کس راستے پر چلوں؟"

        # Default: Human-like interaction
        return "🫡 میں آپ کی بات سمجھ گیا ہوں، لیکن اس پر مزید کام کرنے کے لیے مجھے آپ سے کچھ تفصیلات چاہئیں یا میں خود ریسرچ شروع کروں؟"

