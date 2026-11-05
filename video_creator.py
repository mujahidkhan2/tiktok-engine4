import random

class VideoCreator:
    def __init__(self):
        self.categories = {
            "vlogging": {
                "hooks": ["You won't believe what happened today!", "My daily routine is crazy", "Watch until the end!", "Hidden gem found!"],
                "hashtags": ["#vlog", "#daily", "#lifestyle", "#trending", "#explore"]
            },
            "tech": {
                "hooks": ["This gadget changes everything!", "Top 3 tech tips for you", "Stop using your phone wrong!", "Future of AI is here"],
                "hashtags": ["#tech", "#gadgets", "#innovation", "#ai", "#smarttech"]
            },
            "funny": {
                "hooks": ["Wait for the twist!", "I can't stop laughing", "Tag a friend who does this", "Relatable moment!"],
                "hashtags": ["#funny", "#comedy", "#lol", "#humor", "#memes"]
            },
            "general": {
                "hooks": ["Check this out!", "Interesting find!", "Amazing view", "Something new for you"],
                "hashtags": ["#fyp", "#viral", "#trending", "#explore", "#foryou"]
            }
        }

    def generate_metadata(self, account_identity):
        bio = account_identity.get("bio", "").lower()
        category = "general"
        
        if "vlog" in bio or "life" in bio: category = "vlogging"
        elif "tech" in bio or "ai" in bio: category = "tech"
        elif "funny" in bio or "joke" in bio: category = "funny"

        cat_data = self.categories[category]
        return {
            "category": category,
            "hook": random.choice(cat_data["hooks"]),
            "hashtags": " ".join(random.sample(cat_data["hashtags"], 3)),
            "caption": f"{random.choice(cat_data['hooks'])} {random.choice(cat_data['hashtags'])}"
        }