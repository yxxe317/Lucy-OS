"""
Quantum Algorithms - Simulated quantum computing
"""

import math
import random
import numpy as np
from typing import List, Dict, Optional, Tuple

class QuantumAlgorithm:
    """
    Simulated quantum algorithms for enhanced computation
    """
    
    def __init__(self, n_qubits: int = 4):
        self.n_qubits = n_qubits
        self.state = np.zeros(2**n_qubits, dtype=complex)
        self.state[0] = 1.0  # Initialize to |0...0>
        self.gates = {
            'h': self._hadamard,
            'x': self._paulix,
            'y': self._pauliy,
            'z': self._pauliz,
            'cx': self._cnot,
            'swap': self._swap
        }
        self.measurement_history = []
    
    def _hadamard(self, qubit: int):
        """Apply Hadamard gate"""
        size = 2**self.n_qubits
        new_state = np.zeros(size, dtype=complex)
        for i in range(size):
            if self.state[i] != 0:
                # Find states that differ in target qubit
                mask = 1 << qubit
                partner = i ^ mask
                new_state[i] += self.state[i] / math.sqrt(2)
                new_state[partner] += self.state[i] / math.sqrt(2)
        self.state = new_state
    
    def _paulix(self, qubit: int):
        """Apply Pauli-X (NOT) gate"""
        mask = 1 << qubit
        for i in range(len(self.state)):
            if self.state[i] != 0:
                partner = i ^ mask
                if partner > i:  # Avoid double swapping
                    self.state[i], self.state[partner] = self.state[partner], self.state[i]
    
    def _pauliy(self, qubit: int):
        """Apply Pauli-Y gate"""
        mask = 1 << qubit
        for i in range(len(self.state)):
            if self.state[i] != 0:
                partner = i ^ mask
                phase = 1j if (i >> qubit) & 1 else -1j
                self.state[partner] += phase * self.state[i]
                self.state[i] = 0
    
    def _pauliz(self, qubit: int):
        """Apply Pauli-Z gate"""
        for i in range(len(self.state)):
            if self.state[i] != 0 and (i >> qubit) & 1:
                self.state[i] *= -1
    
    def _cnot(self, control: int, target: int):
        """Apply CNOT gate"""
        for i in range(len(self.state)):
            if self.state[i] != 0 and (i >> control) & 1:
                mask = 1 << target
                partner = i ^ mask
                self.state[i], self.state[partner] = self.state[partner], self.state[i]
    
    def _swap(self, q1: int, q2: int):
        """Apply SWAP gate"""
        for i in range(len(self.state)):
            if self.state[i] != 0:
                b1 = (i >> q1) & 1
                b2 = (i >> q2) & 1
                if b1 != b2:
                    mask = (1 << q1) | (1 << q2)
                    partner = i ^ mask
                    self.state[i], self.state[partner] = self.state[partner], self.state[i]
    
    def apply_gate(self, gate: str, *args):
        """Apply quantum gate"""
        if gate in self.gates:
            self.gates[gate](*args)
    
    def measure(self, qubit: int = None) -> int:
        """
        Measure a qubit (collapse superposition)
        """
        if qubit is None:
            # Measure all qubits
            probabilities = np.abs(self.state)**2
            outcome = np.random.choice(len(self.state), p=probabilities)
            self.state = np.zeros_like(self.state)
            self.state[outcome] = 1.0
            self.measurement_history.append(outcome)
            return outcome
        else:
            # Measure single qubit
            prob_one = 0
            for i in range(len(self.state)):
                if (i >> qubit) & 1:
                    prob_one += np.abs(self.state[i])**2
            
            outcome = 1 if random.random() < prob_one else 0
            
            # Collapse state
            new_state = np.zeros_like(self.state)
            norm = 0
            for i in range(len(self.state)):
                if ((i >> qubit) & 1) == outcome:
                    new_state[i] = self.state[i]
                    norm += np.abs(self.state[i])**2
            
            if norm > 0:
                self.state = new_state / math.sqrt(norm)
            
            self.measurement_history.append(outcome)
            return outcome
    
    def grover_search(self, target_func, n_iterations: int = None):
        """
        Grover's search algorithm
        """
        n = self.n_qubits
        N = 2**n
        
        # Initialize superposition
        for q in range(n):
            self.apply_gate('h', q)
        
        if n_iterations is None:
            n_iterations = int(math.pi/4 * math.sqrt(N))
        
        for _ in range(n_iterations):
            # Oracle
            for i in range(N):
                if target_func(i):
                    self.state[i] *= -1
            
            # Diffusion
            for q in range(n):
                self.apply_gate('h', q)
            for q in range(n):
                self.apply_gate('x', q)
            
            # Multi-controlled Z
            self.state[0] *= -1
            
            for q in range(n):
                self.apply_gate('x', q)
            for q in range(n):
                self.apply_gate('h', q)
        
        # Measure
        return self.measure()
    
    def quantum_fourier_transform(self):
        """
        Quantum Fourier Transform
        """
        n = self.n_qubits
        for i in range(n):
            self.apply_gate('h', i)
            for j in range(i + 1, n):
                # Apply controlled phase rotation
                k = j - i
                phase = math.exp(2 * math.pi * 1j / (2**(k+1)))
                for state_idx in range(len(self.state)):
                    if (state_idx >> i) & 1 and (state_idx >> j) & 1:
                        self.state[state_idx] *= phase
    
    def get_probabilities(self) -> List[float]:
        """Get measurement probabilities"""
        return np.abs(self.state)**2
    
    def get_state_string(self) -> str:
        """Get string representation of quantum state"""
        result = []
        for i, amp in enumerate(self.state):
            if np.abs(amp) > 1e-10:
                bits = format(i, f'0{self.n_qubits}b')
                result.append(f"{amp:.3f}|{bits}>")
        return " + ".join(result)