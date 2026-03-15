# test_language_simple.py
from language.translator import Translator
from language.creative import CreativeWriter
from language.summarizer import TextSummarizer
from language.negotiator import Negotiator
from language.tutor import LanguageTutor

print("="*50)
print("TESTING LUCY LANGUAGE MODULES (SIMPLIFIED)")
print("="*50)

# Test Translator
print("\n1. Testing Translator...")
t = Translator()
translation = t.translate("hello", "es")
print(f"✓ hello -> Spanish: {translation}")

# Test Creative Writer
print("\n2. Testing Creative Writer...")
writer = CreativeWriter()
haiku = writer.generate_haiku("nature")
print(f"✓ Haiku:\n{haiku}")

# Test Summarizer
print("\n3. Testing Summarizer...")
summarizer = TextSummarizer()
long_text = "This is a very long text that needs to be summarized. It contains multiple sentences. Each one adds more information. The summarizer should pick the most important ones."
summary = summarizer.summarize(long_text, ratio=0.5)
print(f"✓ Summary: {summary}")

# Test Negotiator
print("\n4. Testing Negotiator...")
negotiator = Negotiator()
result = negotiator.negotiate("price", {"price": 100}, {"price": 80})
print(f"✓ Negotiation success: {result['success']}")

# Test Tutor
print("\n5. Testing Language Tutor...")
tutor = LanguageTutor()
lesson = tutor.get_lesson("es")
print(f"✓ Spanish lesson: {len(lesson['words'])} words")

print("\n" + "="*50)
print("✓ LANGUAGE TESTS COMPLETE")
print("="*50)