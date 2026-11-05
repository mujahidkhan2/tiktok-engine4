import random
import time

class TrustBuilder:
    def __init__(self, engine):
        self.engine = engine
        # انسانی رویے کے لیے کمنٹس اور ایموجیز کا ڈیٹا بیس (مزید وسعت دی گئی)
        self.positive_comments = [
            "Amazing!", "Love this ❤️", "Wow, so cool!", "Keep it up!", 
            "Very helpful", "Nice video 🔥", "I didn't know this!", 
            "So true!", "Absolutely love it!", "Perfect timing!"
        ]
        self.emojis = ["❤️", "🔥", "👏", "😍", "🙌", "✨", "💯", "🤩", "👍", "🚀"]

    def perform_human_actions(self, account, mode='Active'):
        """
        HIGH-LEVEL LOGICAL SIMULATION:
        Actions now follow a human pattern (Watch -> Like -> Comment) 
        instead of random jumps.
        """
        username = account.get('username', 'Unknown')
        
        # موڈ کے مطابق سیشن کی شدت (Intensity) طے کرنا
        if mode == 'aggressive':
            sessions = random.randint(4, 8)  # زیادہ سیشنز
            action_depth = 'deep'           # ہر سیشن میں گہرا اثر
        elif mode == 'passive':
            sessions = random.randint(1, 3)  # بہت کم سیشنز
            action_depth = 'shallow'        # صرف اوپر اوپر سے دیکھنا
        elif mode == 'curious':
            sessions = random.randint(3, 6)
            action_depth = 'profile'        # پروفائلز پر زیادہ توجہ
        else: # minimal
            sessions = random.randint(1, 2)
            action_depth = 'surface'        # صرف سکرولنگ

        print(f"🛠️ {username} starting {mode} session: {sessions} activities planned...")
        
        for s in range(sessions):
            # --- LOGICAL FLOW STARTS HERE ---
            # ہر سیشن میں ایک "منطقی کہانی" ہوگی
            
            # 1. ہر سیشن کی شروعات ہمیشہ سکرولنگ سے ہوگی
            self.random_scroll(account)
            
            # 2. اب طے کریں گے کہ کیا یہ ویڈیو اسے پسند آئی؟
            interest_level = random.random()
            
            if interest_level > 0.7: # بہت زیادہ دلچسپی (Deep Interaction)
                self.watch_and_like(account)
                if random.random() > 0.4: # 60% چانس کہ کمنٹ بھی کرے
                    self.smart_comment(account)
                if random.random() > 0.7: # 30% چانس کہ سیو بھی کرے
                    self.save_video(account)
                    
            elif interest_level > 0.3: # درمیانی دلچسپی (Shallow Interaction)
                self.watch_and_like(account)
                
            else: # کوئی دلچسپی نہیں، بس آگے بڑھ گیا
                print(f"⏭️ {username} found the video boring and skipped.")
            
            # 3. سیشن کے آخر میں کبھی کبھار پروفائل یا سیٹنگز چیک کرنا
            if action_depth == 'profile' or random.random() > 0.8:
                self.interact_with_profile(account)
            
            if random.random() > 0.9:
                self.visit_settings(account)

            # دو سیشنز کے درمیان ایک لمبا انسانی وقفہ
            break_time = random.uniform(30, 120)
            print(f"☕ {username} taking a short break for {int(break_time)}s...")
            time.sleep(break_time)

    def random_scroll(self, account):
        watch_time = random.uniform(5, 25) 
        print(f"📱 {account['username']} scrolling... Watched for {int(watch_time)}s")
        time.sleep(watch_time)

    def watch_and_like(self, account):
        view_time = random.uniform(15, 45) # لائک کرنے سے پہلے مکمل دیکھنا ضروری ہے
        print(f"👁️ {account['username']} deeply watching... {int(view_time)}s... ❤️ LIKED!")
        time.sleep(view_time)

    def smart_comment(self, account):
        # کمنٹ کرنے سے پہلے تھوڑا سوچنے کا وقفہ (Human Pause)
        thinking_time = random.uniform(5, 15)
        time.sleep(thinking_time)
        
        if random.random() > 0.5:
            comment = random.choice(self.positive_comments)
            print(f"💬 {account['username']} typed: '{comment}'")
        else:
            emoji = random.choice(self.emojis)
            print(f"💬 {account['username']} sent emoji: {emoji}")
        time.sleep(random.uniform(3, 8))

    def interact_with_profile(self, account):
        action_type = random.choice(['visit', 'follow'])
        if action_type == 'follow':
            print(f"👤 {account['username']} checked profile and FOLLOWED.")
        else:
            print(f"👤 {account['username']} read the profile bio.")
        time.sleep(random.uniform(10, 20))

    def visit_settings(self, account):
        print(f"⚙️ {account['username']} updating account preferences...")
        time.sleep(random.uniform(15, 30))

    def save_video(self, account):
        print(f"💾 {account['username']} saved video to 'Favorites'.")
        time.sleep(random.uniform(5, 10))
