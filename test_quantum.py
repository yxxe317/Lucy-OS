# test_quantum.py
from quantum.quantum_algorithm import QuantumAlgorithm
from quantum.entanglement import QuantumEntanglement
from quantum.quantum_memory import QuantumMemory
from quantum.quantum_decision import QuantumDecision
from quantum.quantum_sim import QuantumSimulator

print("="*60)
print("🧪 TESTING QUANTUM MODULES")
print("="*60)

# ==================== TEST QUANTUM ALGORITHM ====================
print("\n⚛️ 1. TESTING QUANTUM ALGORITHM")
print("-" * 40)

qa = QuantumAlgorithm(n_qubits=3)
print(f"✅ Initial state: {qa.get_state_string()}")

qa.apply_gate('h', 0)
qa.apply_gate('h', 1)
print(f"✅ After Hadamard: {qa.get_state_string()}")

probs = qa.get_probabilities()
print(f"✅ Probabilities: {probs}")

result = qa.measure()
print(f"✅ Measurement result: {result}")

# ==================== TEST ENTANGLEMENT ====================
print("\n\n🔗 2. TESTING QUANTUM ENTANGLEMENT")
print("-" * 40)

qe = QuantumEntanglement()

pair_id = qe.create_bell_pair(0, 1)
print(f"✅ Created Bell pair: {pair_id}")

result1, result2 = qe.measure_correlated(pair_id)
print(f"✅ Correlated measurement: {result1}, {result2}")

result1, result2 = qe.measure_anticorrelated(pair_id)
print(f"✅ Anticorrelated measurement: {result1}, {result2}")

teleported = qe.teleport(1, 0, pair_id)
print(f"✅ Teleported state: {teleported}")

bell_test = qe.violate_bell_inequality()
print(f"✅ Bell inequality test: Win prob = {bell_test['win_probability']:.3f}")
print(f"   Quantum violation: {bell_test['quantum_violation']}")

# ==================== TEST QUANTUM MEMORY ====================
print("\n\n💾 3. TESTING QUANTUM MEMORY")
print("-" * 40)

qm = QuantumMemory()

import numpy as np
state_id = qm.store_state(np.array([1, 0, 0, 0], dtype=complex))
print(f"✅ Stored quantum state: {state_id}")

sup_id = qm.store_superposition(
    ['A', 'B', 'C', 'D'],
    [0.1, 0.2, 0.3, 0.4]
)
print(f"✅ Stored superposition: {sup_id}")

qm.entangle(state_id, sup_id)
entangled = qm.get_entangled_states(state_id)
print(f"✅ Entangled states: {entangled}")

collapsed = qm.collapse(sup_id)
print(f"✅ Collapsed superposition to: {collapsed}")

coherence = qm.measure_coherence(state_id)
print(f"✅ Coherence: {coherence:.3f}")

search_result = qm.quantum_search(lambda x: x == 42, 100)
print(f"✅ Quantum search result: {search_result}")

entropy = qm.get_quantum_entropy()
print(f"✅ Quantum entropy: {entropy:.3f}")

# ==================== TEST QUANTUM DECISION ====================
print("\n\n🤔 4. TESTING QUANTUM DECISION")
print("-" * 40)

qd = QuantumDecision()

options = ['coffee', 'tea', 'water', 'juice']
choice = qd.superposition_choice(options)
print(f"✅ Superposition choice: {choice}")

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
path = qd.quantum_walk(graph, steps=5)
print(f"✅ Quantum walk: {' -> '.join(path)}")

good_options = ['coffee', 'tea']
choice = qd.amplitude_amplification(good_options, options)
print(f"✅ Amplitude amplification: {choice}")

choice1 = qd.entangled_decision('dec1', options)
choice2 = qd.entangled_decision('dec2', options, partner_id='dec1')
print(f"✅ Entangled decisions: {choice1}, {choice2}")

universes = qd.parallel_universe_choice(options[:3])
print(f"✅ Parallel universes: {len(universes)} explored")

barriers = [0.5, 1.5, 0.8, 2.0]
choice = qd.quantum_tunnel_choice(options[:4], barriers)
print(f"✅ Quantum tunnel choice: {choice}")

entropy = qd.get_decision_entropy()
print(f"✅ Decision entropy: {entropy:.3f}")

# ==================== TEST QUANTUM SIMULATOR ====================
print("\n\n🖥️ 5. TESTING QUANTUM SIMULATOR")
print("-" * 40)

qs = QuantumSimulator(n_qubits=3)
print(f"✅ Initialized {qs.n_qubits}-qubit simulator")

qs.hadamard(0)
qs.hadamard(1)
qs.cnot(0, 1)
print(f"✅ Applied gates")

probs = qs.get_probabilities()
print(f"✅ Probabilities: {probs[:4]}...")

result = qs.measure()
print(f"✅ Measurement: {result}")

purity = qs.get_purity()
print(f"✅ Purity: {purity:.3f}")

entropy = qs.get_entropy()
print(f"✅ Entropy: {entropy:.3f}")

qs.simulate_decoherence(rate=0.1)
print(f"✅ Simulated decoherence")

gate_stats = qs.get_gate_statistics()
print(f"✅ Gate statistics: {gate_stats}")

grover_result = qs.run_algorithm('grover', target=5, n_items=16)
print(f"✅ Grover search: {grover_result['success']}")

print("\n" + "="*60)
print("✅ QUANTUM TESTS COMPLETE")
print("="*60)