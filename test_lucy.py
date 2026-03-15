# test_lucy.py
from memory.long_term import LongTermMemory
from memory.working import WorkingMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
from memory.memory_palace import MemoryPalace

print("="*50)
print("TESTING LUCY MEMORY MODULES")
print("="*50)

# Test LongTermMemory
print("\n1. Testing LongTermMemory...")
ltm = LongTermMemory("test_memory.db")
ltm.store_conversation("user123", "user", "Hello Lucy!")
ltm.store_conversation("user123", "lucy", "Hi there! How can I help?")
history = ltm.get_conversation_history("user123")
print(f"   ✓ Stored {len(history)} conversations")
for msg in history:
    print(f"   - {msg['role']}: {msg['content'][:30]}...")

# Test WorkingMemory
print("\n2. Testing WorkingMemory...")
wm = WorkingMemory(capacity=5)
wm.add({"role": "user", "content": "What's the weather?"}, "msg1")
wm.add({"role": "lucy", "content": "Checking weather..."}, "msg2")
item = wm.get("msg1")
print(f"   ✓ Retrieved: {item['content']}")
print(f"   ✓ Working memory size: {len(wm.get_all())}")

# Test EpisodicMemory
print("\n3. Testing EpisodicMemory...")
em = EpisodicMemory("test_episodic.db")
ep_id = em.start_episode("user123")
em.add_message(ep_id, "user", "Tell me a joke")
em.add_message(ep_id, "lucy", "Why did the chicken cross the road?")
em.add_message(ep_id, "user", "I don't know, why?")
em.add_message(ep_id, "lucy", "To get to the other side!")
episodes = em.get_recent_episodes("user123")
print(f"   ✓ Created episode with {len(episodes[0]['messages'])} messages")

# Test SemanticMemory
print("\n4. Testing SemanticMemory...")
sm = SemanticMemory("test_semantic.db")
sm.store("Paris is the capital of France", "geography", confidence=0.95)
sm.store("The Eiffel Tower is in Paris", "landmarks")
facts = sm.recall("capital of France")
print(f"   ✓ Found {len(facts)} facts")
for fact in facts:
    print(f"   - {fact['fact']} (confidence: {fact['confidence']})")

# Test MemoryPalace
print("\n5. Testing MemoryPalace...")
palace = MemoryPalace()
palace.place_memory("fact1", {"type": "fact", "content": "Earth orbits Sun"})
palace.place_memory("fact2", {"type": "fact", "content": "Moon orbits Earth"}, 
                    room="library", location="shelves")
print(palace.visualize())

print("\n" + "="*50)
print("✓ ALL TESTS COMPLETE")
print("="*50)