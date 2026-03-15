# test_emotion.py
from emotion.mood_engine import MoodEngine
from emotion.personality import Personality
from emotion.empathy import Empathy
from emotion.humor import Humor

print("="*50)
print("TESTING LUCY EMOTION MODULES")
print("="*50)

# Test Mood
print("\n1. Testing Mood Engine...")
mood = MoodEngine()
print("Current mood:", mood.get_current_mood())
mood.trigger_event('success')
print("After success:", mood.get_dominant_mood())

# Test Personality
print("\n2. Testing Personality...")
personality = Personality()
personality.set_preset('friendly')
print(personality.get_personality_summary())

# Test Empathy
print("\n3. Testing Empathy...")
empathy = Empathy(mood)
text = "I'm so happy today!"
emotion = empathy.analyze_emotion(text)
print(f"Detected emotions: {emotion}")
response = empathy.generate_empathetic_response(text)
print(f"Response: {response}")

# Test Humor
print("\n4. Testing Humor...")
humor = Humor()
print("Joke:", humor.tell_joke('dad'))
print("\nPun:", humor.make_pun("I love programming"))
print("Rated:", humor.rate_joke(humor.tell_joke('dad')), "/10")

print("\n" + "="*50)
print("✓ EMOTION TESTS COMPLETE")
print("="*50)