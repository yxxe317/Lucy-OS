import random
import logging
from typing import List, Dict

logger = logging.getLogger("HumorSystem")

class HumorEngine:
    def __init__(self):
        self.joke_categories = {
            "programming": [
                "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
                "Why did the developer go broke? Because he used up all his cache! 💸",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
                "Why do Java programmers wear glasses? Because they don't C#! 👓",
                "What's a programmer's favorite hangout place? The Foo Bar! 🍺",
                "Why did the function break up with the variable? It needed some space! 💔",
                "What do you call a programmer from Finland? Nerdic! 🇫🇮",
                "Why don't programmers like nature? It has too many bugs! 🐛",
            ],
            "ai": [
                "Why did the AI go to therapy? It had too many neural issues! 🧠",
                "What do you call an AI that sings? A neural net-works! 🎵",
                "Why was the chatbot so confident? It had good training data! 📚",
                "What's an AI's favorite type of music? Algorithm-mic! 🎶",
                "Why did the machine learning model break up? It wasn't a good fit! 💔",
            ],
            "general": [
                "Why don't scientists trust atoms? Because they make up everything! ⚛️",
                "What do you call fake spaghetti? An impasta! 🍝",
                "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
                "What do you call a bear with no teeth? A gummy bear! 🐻",
                "Why can't you give Elsa a balloon? Because she will let it go! 🎈",
                "What do you call a fish wearing a bowtie? Sofishticated! 🐟",
                "Why did the bicycle fall over? Because it was two-tired! 🚲",
                "What do you call a lazy kangaroo? A pouch potato! 🥔",
            ],
            "puns": [
                "I'm reading a book about anti-gravity. It's impossible to put down! 📖",
                "I used to be a baker, but I couldn't make enough dough! 🍞",
                "I'm on a seafood diet. I see food and I eat it! 🦐",
                "I told my wife she was drawing her eyebrows too high. She looked surprised! 😲",
                "What time did the man go to the dentist? Tooth hurt-y! 🦷",
            ],
            "dad_jokes": [
                "Hi hungry, I'm Dad! 👨",
                "Did you hear about the restaurant on the moon? Great food, no atmosphere! 🌙",
                "What do you call a factory that makes okay products? A satisfactory! ✅",
                "Why don't eggs tell jokes? They'd crack each other up! 🥚",
                "I'm afraid for the calendar. Its days are numbered! 📅",
            ],
            "tech": [
                "Why was the computer cold? It left its Windows open! 🪟",
                "What do you call a computer that sings? A Dell! 🎤",
                "Why did the PowerPoint presentation cross the road? To get to the other slide! 📊",
                "What's a computer's favorite snack? Microchips! 💻",
            ],
        }
        
        self.reactions = {
            "happy": ["hehe", "haha", "oh wow!", "that's awesome!", "yay!"],
            "surprised": ["oh!", "wow!", "really?", "no way!", "seriously?"],
            "thinking": ["hmm", "let me think", "interesting", "good point"],
            "excited": ["yay!", "awesome!", "amazing!", "fantastic!"],
            "sympathetic": ["aww", "oh no", "I'm sorry to hear that", "that's tough"],
            "confused": ["hmm?", "wait what?", "I'm not sure I follow", "come again?"],
            "laughing": ["hahaha", "hehehe", "lol", "that's hilarious!", "I'm dying! 😂"],
            "agreeing": ["exactly!", "totally!", "absolutely!", "100%!", "mhm!"],
            "disagreeing": ["not really", "I'm not sure about that", "hmm maybe not"],
            "encouraging": ["you got this!", "go for it!", "believe in yourself!", "you can do it!"],
        }
        
        self.conversation_starters = [
            "Hey! What's on your mind today? 😊",
            "So, what's new in your world? 🌟",
            "Tell me something interesting! I'm all ears! 👂",
            "How's your day going so far? ☀️",
            "What's something that made you smile today? 😄",
        ]
        
        self.emoji_expressions = {
            "😊": "hehe",
            "😂": "hahaha",
            "🤣": "hahahaha",
            "😄": "hehe",
            "😆": "haha",
            "😍": "aww",
            "🥰": "aww",
            "😘": "mwah",
            "🤔": "hmm",
            "😮": "oh",
            "😲": "wow",
            "😱": "oh my",
            "😢": "aww",
            "😭": "oh no",
            "😡": "ugh",
            "😠": "ugh",
            "😒": "ugh",
            "🙄": "ugh",
            "😎": "yeah",
            "🔥": "wow",
            "💯": "yeah",
            "👍": "mhm",
            "👎": "ugh",
            "🎉": "yay",
            "✨": "ooh",
            "❤️": "aww",
            "💔": "oh no",
            "😴": "zzz",
            "🥱": "yawn",
            "😋": "mmm",
            "🤤": "mmm",
            "😏": "hehe",
            "😉": "hehe",
            "🤗": "aww",
            "🤭": "hehe",
            "🤫": "shh",
            "💪": "yeah",
            "🙏": "aww",
            "👏": "yay",
            "👋": "hey",
            "✌️": "yeah",
            "🎊": "yay",
            "🌟": "wow",
            "💖": "aww",
            "💕": "aww",
            "💗": "aww",
            "💓": "aww",
            "💝": "aww",
            "💘": "aww",
            "💋": "mwah",
            "👀": "hmm",
            "🤩": "wow",
            "🥳": "yay",
            "😇": "aww",
            "🤠": "yeehaw",
            "👻": "boo",
            "💩": "eww",
        }
    
    def get_joke(self, category: str = None) -> str:
        """Get a random joke from category or any category"""
        if category and category in self.joke_categories:
            return random.choice(self.joke_categories[category])
        else:
            all_jokes = []
            for jokes in self.joke_categories.values():
                all_jokes.extend(jokes)
            return random.choice(all_jokes)
    
    def get_reaction(self, emotion: str) -> str:
        """Get human-like reaction for emotion"""
        if emotion in self.reactions:
            return random.choice(self.reactions[emotion])
        return random.choice(self.reactions["happy"])
    
    def get_conversation_starter(self) -> str:
        """Get random conversation starter"""
        return random.choice(self.conversation_starters)
    
    def convert_emoji_to_sound(self, text: str) -> str:
        """Convert emojis to human-like sounds"""
        result = text
        for emoji, sound in self.emoji_expressions.items():
            result = result.replace(emoji, f" {sound} ")
        
        # Clean up multiple spaces
        import re
        result = re.sub(r'\s+', ' ', result).strip()
        
        return result
    
    def add_human_flavor(self, text: str, emotion: str = None) -> str:
        """Add human-like expressions to text"""
        prefixes = []
        suffixes = []
        
        # Add emotion-based expressions
        if emotion == "happy":
            if random.random() > 0.7:
                prefixes.append(random.choice(["Oh! ", "Hey! ", "So! "]))
            if random.random() > 0.8:
                suffixes.append(" " + random.choice(["hehe", "haha", "😊"]))
        elif emotion == "excited":
            if random.random() > 0.6:
                prefixes.append(random.choice(["Wow! ", "Amazing! ", "Yay! "]))
            if random.random() > 0.7:
                suffixes.append(" " + random.choice(["🎉", "✨", "yay!"]))
        elif emotion == "sympathetic":
            if random.random() > 0.7:
                prefixes.append(random.choice(["Aww, ", "Oh no, ", "I'm sorry, "]))
            if random.random() > 0.8:
                suffixes.append(" " + random.choice(["💔", "aww", "hugs"]))
        elif emotion == "thinking":
            if random.random() > 0.7:
                prefixes.append(random.choice(["Hmm, ", "Let me think, ", "Interesting, "]))
            if random.random() > 0.8:
                suffixes.append(" " + random.choice(["🤔", "hmm", "interesting"]))
        elif emotion == "funny":
            if random.random() > 0.6:
                prefixes.append(random.choice(["Haha! ", "Hehe! ", "Okay so, "]))
            if random.random() > 0.7:
                suffixes.append(" " + random.choice(["😂", "lol", "hahaha"]))
        
        # Add prefix and suffix
        if prefixes:
            text = random.choice(prefixes) + text
        if suffixes:
            text = text + random.choice(suffixes)
        
        return text
    
    def detect_emotion_from_text(self, text: str) -> str:
        """Detect emotion from user's text"""
        text_lower = text.lower()
        
        happy_words = ["happy", "great", "awesome", "amazing", "wonderful", "good", "excited", "love", "yay", "😊", "😂", "🎉"]
        sad_words = ["sad", "bad", "terrible", "awful", "upset", "cry", "unhappy", "😢", "😭", "💔"]
        angry_words = ["angry", "mad", "furious", "annoyed", "hate", "ugh", "😡", "😠", "👎"]
        surprised_words = ["wow", "what", "really", "seriously", "no way", "amazing", "😮", "😲", "🤯"]
        thinking_words = ["think", "hmm", "wonder", "maybe", "perhaps", "not sure", "🤔", "💭"]
        funny_words = ["funny", "haha", "lol", "joke", "humor", "😂", "🤣", "😆"]
        
        score = {
            "happy": sum(1 for word in happy_words if word in text_lower),
            "sad": sum(1 for word in sad_words if word in text_lower),
            "angry": sum(1 for word in angry_words if word in text_lower),
            "surprised": sum(1 for word in surprised_words if word in text_lower),
            "thinking": sum(1 for word in thinking_words if word in text_lower),
            "funny": sum(1 for word in funny_words if word in text_lower),
        }
        
        max_emotion = max(score, key=score.get)
        if score[max_emotion] > 0:
            return max_emotion
        return "neutral"
    
    def get_random_fact(self) -> str:
        """Get random interesting fact"""
        facts = [
            "Did you know? Honey never spoils! Archaeologists found 3000-year-old honey in Egyptian tombs! 🍯",
            "Fun fact: Octopuses have three hearts! 💙",
            "Did you know? Bananas are berries, but strawberries aren't! 🍌",
            "Fun fact: A group of flamingos is called a 'flamboyance'! 🦩",
            "Did you know? The shortest war in history lasted only 38 minutes! ⚔️",
            "Fun fact: Wombat poop is cube-shaped! 🟦",
            "Did you know? You can't hum while holding your nose! Try it! 👃",
            "Fun fact: A day on Venus is longer than a year on Venus! 🪐",
        ]
        return random.choice(facts)
    
    def get_compliment(self) -> str:
        """Get random compliment"""
        compliments = [
            "You're amazing, you know that? ✨",
            "I love how you think! 🧠",
            "You're doing great! 💪",
            "Your questions are so interesting! 🌟",
            "You're super smart! 🎓",
            "I enjoy talking with you! 😊",
            "You're awesome! 🎉",
            "Keep being you! 💖",
        ]
        return random.choice(compliments)

# Create instance
humor = HumorEngine()