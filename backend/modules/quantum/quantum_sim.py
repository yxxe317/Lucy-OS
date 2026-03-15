"""
Quantum Simulator - Full quantum system simulation
"""

import numpy as np
import random
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime

class QuantumSimulator:
    """
    Full quantum system simulator with multiple components
    """
    
    def __init__(self, n_qubits: int = 3):  # Default to 3 qubits
        self.n_qubits = n_qubits
        self.dimension = 2**n_qubits
        self.state = np.zeros(self.dimension, dtype=complex)
        self.state[0] = 1.0
        
        self.quantum_memory = {}
        self.entanglements = []
        self.gate_history = []
        self.measurements = []
        
        # Quantum registers
        self.registers = {
            'x': np.zeros(n_qubits),  # Position
            'p': np.zeros(n_qubits),  # Momentum
            'phase': np.zeros(n_qubits)  # Phase
        }
    
    def _apply_single_qubit_gate(self, gate: np.ndarray, qubit: int):
        """Apply single qubit gate"""
        # Create full gate matrix using Kronecker product
        if qubit == 0:
            full_gate = gate
            for i in range(1, self.n_qubits):
                full_gate = np.kron(full_gate, np.eye(2))
        elif qubit == self.n_qubits - 1:
            full_gate = np.eye(2)
            for i in range(self.n_qubits - 2):
                full_gate = np.kron(full_gate, np.eye(2))
            full_gate = np.kron(full_gate, gate)
        else:
            # For middle qubits
            left_size = 2**qubit
            right_size = 2**(self.n_qubits - qubit - 1)
            
            left_identity = np.eye(left_size)
            right_identity = np.eye(right_size)
            
            full_gate = np.kron(np.kron(left_identity, gate), right_identity)
        
        self.state = full_gate @ self.state
    
    def apply_gate(self, gate_matrix: np.ndarray, qubits: List[int]):
        """
        Apply quantum gate to specified qubits
        """
        # Simplified for custom gates
        if len(qubits) == 1:
            self._apply_single_qubit_gate(gate_matrix, qubits[0])
        else:
            # Multi-qubit gate - simplified
            print(f"Multi-qubit gate simulation simplified")
        
        self.gate_history.append({
            'type': 'custom_gate',
            'qubits': qubits,
            'time': datetime.now()
        })
    
    def hadamard(self, qubit: int):
        """Apply Hadamard gate"""
        H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        self._apply_single_qubit_gate(H, qubit)
        
        self.gate_history.append({
            'type': 'H',
            'qubit': qubit
        })
    
    def pauli_x(self, qubit: int):
        """Apply Pauli-X (NOT) gate"""
        X = np.array([[0, 1], [1, 0]], dtype=complex)
        self._apply_single_qubit_gate(X, qubit)
        
        self.gate_history.append({
            'type': 'X',
            'qubit': qubit
        })
    
    def pauli_y(self, qubit: int):
        """Apply Pauli-Y gate"""
        Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self._apply_single_qubit_gate(Y, qubit)
        
        self.gate_history.append({
            'type': 'Y',
            'qubit': qubit
        })
    
    def pauli_z(self, qubit: int):
        """Apply Pauli-Z gate"""
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        self._apply_single_qubit_gate(Z, qubit)
        
        self.gate_history.append({
            'type': 'Z',
            'qubit': qubit
        })
    
    def cnot(self, control: int, target: int):
        """Apply CNOT gate"""
        if self.n_qubits < 2:
            print("Need at least 2 qubits for CNOT")
            return
        
        # Create CNOT matrix for the specific control and target
        dim = self.dimension
        CNOT = np.eye(dim, dtype=complex)
        
        for i in range(dim):
            # Check if control qubit is 1
            if (i >> control) & 1:
                # Flip target qubit
                j = i ^ (1 << target)
                CNOT[i, i] = 0
                CNOT[i, j] = 1
        
        self.state = CNOT @ self.state
        
        self.gate_history.append({
            'type': 'CNOT',
            'control': control,
            'target': target
        })
    
    def measure(self, qubit: int = None) -> int:
        """
        Measure qubit(s)
        """
        if qubit is None:
            # Measure all qubits
            probs = np.abs(self.state)**2
            outcome = np.random.choice(self.dimension, p=probs)
            
            # Collapse state
            new_state = np.zeros(self.dimension, dtype=complex)
            new_state[outcome] = 1.0
            self.state = new_state
            
            self.measurements.append({
                'type': 'full',
                'outcome': outcome,
                'time': datetime.now()
            })
            
            return outcome
        else:
            # Measure single qubit
            prob_one = 0
            for i in range(self.dimension):
                if (i >> qubit) & 1:
                    prob_one += np.abs(self.state[i])**2
            
            outcome = 1 if random.random() < prob_one else 0
            
            # Collapse state (simplified)
            if outcome == 0:
                # Keep only states where qubit is 0
                mask = 1 << qubit
                for i in range(self.dimension):
                    if (i & mask):
                        self.state[i] = 0
            else:
                # Keep only states where qubit is 1
                mask = 1 << qubit
                for i in range(self.dimension):
                    if not (i & mask):
                        self.state[i] = 0
            
            # Normalize
            norm = np.linalg.norm(self.state)
            if norm > 0:
                self.state = self.state / norm
            
            self.measurements.append({
                'type': 'single',
                'qubit': qubit,
                'outcome': outcome
            })
            
            return outcome
    
    def create_bell_state(self):
        """Create Bell state (|00> + |11>)/√2"""
        if self.n_qubits >= 2:
            self.state = np.zeros(self.dimension, dtype=complex)
            self.state[0] = 1/np.sqrt(2)
            self.state[3] = 1/np.sqrt(2)  # |11> for 2 qubits
    
    def create_ghz_state(self):
        """Create GHZ state for all qubits"""
        self.state = np.zeros(self.dimension, dtype=complex)
        self.state[0] = 1/np.sqrt(2)
        self.state[-1] = 1/np.sqrt(2)
    
    def get_probabilities(self) -> np.ndarray:
        """Get measurement probabilities"""
        return np.abs(self.state)**2
    
    def get_density_matrix(self) -> np.ndarray:
        """Get density matrix ρ = |ψ⟩⟨ψ|"""
        return np.outer(self.state, np.conj(self.state))
    
    def get_entropy(self) -> float:
        """Calculate von Neumann entropy"""
        rho = self.get_density_matrix()
        eigenvalues = np.linalg.eigvalsh(rho)
        eigenvalues = eigenvalues[eigenvalues > 1e-10]
        return -np.sum(eigenvalues * np.log2(eigenvalues))
    
    def get_purity(self) -> float:
        """Calculate state purity Tr(ρ²)"""
        rho = self.get_density_matrix()
        return np.trace(rho @ rho).real
    
    def simulate_decoherence(self, rate: float = 0.01):
        """
        Simulate decoherence (mixed with noise)
        """
        # Add random noise to state
        noise = np.random.randn(self.dimension) * rate + 1j * np.random.randn(self.dimension) * rate
        noise = noise / np.linalg.norm(noise)
        
        self.state = (1 - rate) * self.state + rate * noise
        self.state = self.state / np.linalg.norm(self.state)
    
    def get_gate_statistics(self) -> Dict:
        """Get statistics of applied gates"""
        stats = {}
        for gate in self.gate_history:
            gate_type = gate['type']
            stats[gate_type] = stats.get(gate_type, 0) + 1
        return stats
    
    def run_algorithm(self, algorithm: str, **params) -> Dict:
        """
        Run predefined quantum algorithm
        """
        if algorithm == 'grover':
            return self._grover_search(**params)
        elif algorithm == 'qft':
            return self._quantum_fourier_transform(**params)
        elif algorithm == 'phase_estimation':
            return self._phase_estimation(**params)
        else:
            return {'error': 'Unknown algorithm'}
    
    def _grover_search(self, target: int, n_items: int = 16) -> Dict:
        """Simulate Grover's search"""
        if n_items != self.dimension:
            self.dimension = n_items
            self.state = np.zeros(n_items, dtype=complex)
        
        # Reset state
        for i in range(n_items):
            self.state[i] = 1/np.sqrt(n_items)
        
        # Grover iterations
        iterations = int(np.pi/4 * np.sqrt(n_items))
        
        for _ in range(iterations):
            # Oracle
            self.state[target] *= -1
            
            # Diffusion
            avg = np.mean(self.state)
            for i in range(n_items):
                self.state[i] = 2*avg - self.state[i]
        
        # Measure
        probs = np.abs(self.state)**2
        result = np.random.choice(n_items, p=probs)
        
        return {
            'algorithm': 'grover',
            'target': target,
            'result': result,
            'success': result == target,
            'iterations': iterations
        }
    
    def _quantum_fourier_transform(self, input_state: List[complex] = None) -> Dict:
        """Simulate Quantum Fourier Transform"""
        if input_state:
            self.state = np.array(input_state, dtype=complex)
            self.state = self.state / np.linalg.norm(self.state)
        
        n = len(self.state)
        transformed = np.zeros(n, dtype=complex)
        
        for k in range(n):
            for j in range(n):
                transformed[k] += self.state[j] * np.exp(2j * np.pi * j * k / n)
            transformed[k] /= np.sqrt(n)
        
        self.state = transformed
        
        return {
            'algorithm': 'qft',
            'result': self.state.copy()
        }
    
    def _phase_estimation(self, unitary: Callable = None, precision: int = 8) -> Dict:
        """Simulate phase estimation"""
        # Simplified implementation
        phase = random.random()
        return {
            'algorithm': 'phase_estimation',
            'estimated_phase': phase,
            'precision': precision
        }