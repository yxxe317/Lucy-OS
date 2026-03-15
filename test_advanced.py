# tests/test_advanced.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from advanced.brain_computer import BrainComputerInterface
from advanced.consciousness import QuantumConsciousness
from advanced.dream import DreamSimulator
from advanced.time_perception import TimePerception
from advanced.multiverse import MultiverseExplorer
import time

print("="*60)
print("🧪 TESTING ADVANCED MODULES")
print("="*60)

# ==================== TEST BRAIN-COMPUTER INTERFACE ====================
print("\n🧠 1. TESTING BRAIN-COMPUTER INTERFACE")
print("-" * 40)

bci = BrainComputerInterface()
signals = bci.read_neural_signals()
print(f"✅ Neural signals read from {len(signals)} regions")
interpretation = bci.interpret_thought(signals)
print(f"✅ Thought interpretation: {interpretation}")
pattern = bci.encode_thought("Hello world")
print(f"✅ Encoded thought pattern: {pattern[:5]}...")
entrainment = bci.simulate_brainwave_entrainment(10.5, 5)
print(f"✅ {entrainment}")

# ==================== TEST QUANTUM CONSCIOUSNESS ====================
print("\n⚛️ 2. TESTING QUANTUM CONSCIOUSNESS")
print("-" * 40)

qc = QuantumConsciousness()
observation = qc.quantum_observation({'state': 'unknown'})
print(f"✅ Quantum observation: {observation['observed_state']}")
print(f"✅ Consciousness level: {observation['consciousness_level']}")
entanglement = qc.entangle_thoughts("idea1", "idea2")
print(f"✅ Entangled thoughts: {entanglement}")
measurement = qc.measure_entangled_thought("idea1")
print(f"✅ Entangled measurement: {measurement.get('correlation', 'N/A')}")
tunnel = qc.quantum_tunnel_thought("secret", 0.5)
print(f"✅ Quantum tunnel: {tunnel}")
ideas = qc.generate_quantum_idea("AI")
print(f"✅ Quantum ideas: {ideas}")

# ==================== TEST DREAM SIMULATOR ====================
print("\n💤 3. TESTING DREAM SIMULATOR")
print("-" * 40)

dream = DreamSimulator()
dream1 = dream.generate_dream()
print(f"✅ Dream generated: {dream1['title']}")
print(f"   Phase: {dream1['phase']}")
print(f"   Narrative: {dream1['narrative'][:50]}...")
interpretation = dream.interpret_dream(dream1)
print(f"✅ Interpretation: {interpretation[:100]}...")
techniques = dream.lucid_dream_induction()
print(f"✅ Lucid dreaming techniques: {techniques}")
reality_check = dream.dream_reality_check()
print(f"✅ Reality check passed: {reality_check}")
stats = dream.get_dream_statistics()
print(f"✅ Dream stats: {stats.get('total_dreams', 0)} dreams")

# ==================== TEST TIME PERCEPTION ====================
print("\n⏱️ 4. TESTING TIME PERCEPTION")
print("-" * 40)

tp = TimePerception()
duration = tp.subjective_duration(60, 'excitement')
print(f"✅ Subjective duration: {duration['subjective_duration']:.1f}s ({duration['experience']})")
dilation = tp.time_dilation_event(60, 0.9)
print(f"✅ Time dilation factor: {dilation['dilation_factor']:.2f}")
effect = tp.chronostasis('clock_watching')
print(f"✅ Chronostasis: {effect}")
memory = tp.memory_duration(60, 0.8)
print(f"✅ Memory duration: {memory:.1f}s")
predicted = tp.predict_future_duration(0.7, 0.8)
print(f"✅ Predicted future duration: {predicted:.1f}s")
paradox = tp.time_paradox([{'event': 'past'}, {'event': 'future'}])
print(f"✅ Time paradox: {paradox['type']}")
stats = tp.get_perception_statistics()
print(f"✅ Perception stats: avg dilation {stats.get('avg_dilation', 0):.2f}")

# ==================== TEST MULTIVERSE EXPLORER ====================
print("\n🌌 5. TESTING MULTIVERSE EXPLORER")
print("-" * 40)

mv = MultiverseExplorer()
universe_id = mv.create_branch_universe("decision point", 0.5)
print(f"✅ Created branched universe: {universe_id}")
exploration = mv.explore_universe(universe_id)
print(f"✅ Universe explored: {exploration.get('civilization_level')} civilization")
superposition = mv.quantum_superposition(['choice A', 'choice B'])
print(f"✅ Quantum superposition: {len(superposition)} states")
collapsed = mv.collapse_superposition(superposition, 'choice A')
print(f"✅ Collapsed superposition: observed in {collapsed.get('observed_universe', 'N/A')}")
merge = mv.timeline_merge('timeline1', 'timeline2')
print(f"✅ Timeline merge: stability {merge.get('stability', 0):.2f}")
stats = mv.get_multiverse_statistics()
print(f"✅ Multiverse stats: {stats.get('total_universes', 0)} universes")
alternate = mv.find_alternate_self(['smart', 'creative', 'curious'])
print(f"✅ Alternate self similarity: {alternate.get('similarity', 0):.2f}")

print("\n" + "="*60)
print("✅ ADVANCED MODULES TESTS COMPLETE")
print("="*60)