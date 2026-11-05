import random
import time

class TrustBuilder: # نام تبدیل کیا تاکہ engine.py کے ساتھ میچ کرے
    def __init__(self, engine):
        self.engine = engine
        # انسانی رویے کے لیے کمنٹس اور ایموجیز کا ڈیٹا بیس
        self.positive_comments = ["Amazing!", "Love this ❤️", "Wow, so cool!", "Keep it up!", "Very helpful", "Nice video 🔥"]
        self.emojis = ["❤️", "🔥", "👏", "😍", "🙌", "✨", "💯"]

    def perform_human_actions(self, account, mode='Active'):
        """
        High-Level Human Simulation: Mode-based behavior to fool the algorithm.
        """
        username = account.get('username', 'Unknown')
        
        # موڈ کے مطابق ایکشنز کی لسٹ طے کرنا
        if mode == 'aggressive':
            # بہت زیادہ ایکشنز: سکرولنگ، لائک، کمنٹ، اور سیو سب کچھ
            available_actions = [
                self.random_scroll, self.watch_and_like, self.smart_comment, 
                self.interact_with_profile, self.visit_settings, self.save_video
            ]
            num_actions = random.randint(6, 12) # زیادہ کام
        elif mode == 'passive':
            # کم ایکشنز: صرف دیکھنا اور کبھی کبھار لائک کرنا
            available_actions = [self.random_scroll, self.watch_and_like, self.visit_settings]
            num_actions = random.randint(2, 4) # کم کام
        elif mode == 'curious':
            # پروفائلز اور سیٹنگز زیادہ چیک کرنا
            available_actions = [self.interact_with_profile, self.visit_settings, self.random_scroll]
            num_actions = random.randint(4, 8)
        else: # minimal
            available_actions = [self.random_scroll, self.visit_settings]
            num_actions = random.randint(1, 3)

        print(f"🛠️ {username} starting session in {mode} mode ({num_actions} actions)...")
        
        for i in range(num_actions):
            action = random.choice(available_actions)
            # ہر ایکشن کو اکاؤنٹ کا ڈیٹا پاس کریں
            action(account)
            
            # ایکشنز کے درمیان انسانی وقفہ (رینڈم)
            # بعض اوقات انسان جلدی کرتا ہے، بعض اوقات دیر لگاتا ہے
            gap = random.uniform(15, 45) 
            time.sleep(gap)

    def random_scroll(self, account):
        # صرف سکرول نہیں، بلکہ 'واچ ٹائم' کا تعین
        watch_time = random.uniform(3, 30) # 3 سیکنڈ سے 30 سیکنڈ تک ویڈیو دیکھنا
        print(f"📱 {account['username']} scrolling... Watched a video for {int(watch_time)}s")
        time.sleep(watch_time)

    def watch_and_like(self, account):
        # پہلے ویڈیو دیکھے، پھر لائک کرے (جیسے انسان کرتا ہے)
        view_time = random.uniform(10, 40)
        print(f"👁️ {account['username']} watching video for {int(view_time)}s... then LIKED it! ❤️")
        time.sleep(view_time)

    def smart_comment(self, account):
        # رینڈم کمنٹ یا صرف ایموجی
        if random.random() > 0.5:
            comment = random.choice(self.positive_comments)
            print(f"💬 {account['username']} commented: '{comment}'")
        else:
            emoji = random.choice(self.emojis)
            print(f"💬 {account['username']} commented an emoji: {emoji}")
        time.sleep(random.uniform(5, 12))

    def interact_with_profile(self, account):
        # پروفائل دیکھنا اور شاید فالو کرنا
        action_type = random.choice(['visit', 'follow'])
        if action_type == 'follow':
            print(f"👤 {account['username']} visited profile and FOLLOWED.")
        else:
            print(f"👤 {account['username']} just checked the profile bio.")
        time.sleep(random.uniform(8, 20))

    def visit_settings(self, account):
        # سیٹنگز میں جا کر کچھ سیکنڈ رکنا
        print(f"⚙️ {account['username']} is adjusting privacy/account settings...")
        time.sleep(random.uniform(10, 25))

    def save_video(self, account):
        print(f"💾 {account['username']} saved a high-value video to favorites.")
        time.sleep(random.uniform(5, 10))