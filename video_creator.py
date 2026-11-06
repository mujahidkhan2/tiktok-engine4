import random

class VideoCreator:
    def __init__(self):
        self.categories = {
            "USA": ["tech_reviews", "lifestyle_vlogs", "fitness_tips", "home_decor"],
            "UK": ["fashion_trends", "travel_hacks", "cooking_shorts", "minimalism"],
            "PK": ["food_vlogs", "street_life", "tech_urdu", "nature"]
        }

    def generate_content_plan(self, country):
        category = random.choice(self.categories.get(country, ["general"]))
        return {
            "category": category,
            "style": random.choice(["fast_paced", "aesthetic", "educational"]),
            "duration": random.randint(15, 58)
        }

    def create_unique_video_metadata(self, account_id, country):
        plan = self.generate_content_plan(country)
        hashtags_db = {
            "tech_reviews": ["#tech", "#gadgets", "#innovation"],
            "lifestyle_vlogs": ["#dailyvlog", "#lifestyle", "#routine"],
            "fashion_trends": ["#ootd", "#fashionuk", "#style"],
            "home_decor": ["#homedecor", "#interior", "#usa_homes"],
            "food_vlogs": ["#foodie", "#streetfood", "#delicious"]
        }
        hashtags = hashtags_db.get(plan["category"], ["#trending", "#fyp"])
        caption = f"{random.choice(['Amazing', 'Must see', 'Wow'])} {random.choice(hashtags)}!"
        
        return {
            "account_id": account_id,
            "caption": caption,
            "hashtags": random.sample(hashtags, 2),
            "category": plan["category"],
            "duration": plan["duration"]
        }
