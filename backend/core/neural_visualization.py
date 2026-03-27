"""
Neural Visualization Module - Visualize AI decision paths and attention flows
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
import random

class NeuralVisualizer:
    def __init__(self):
        self.visualization_log = Path("data/neural_viz")
        self.visualization_log.mkdir(exist_ok=True)
        self.decision_graphs = []
    
    def generate_attention_map(self, query: str, context: list) -> dict:
        """Generate simulated attention weight distribution"""
        words = query.split()
        attention_weights = {}
        
        for i, word in enumerate(words):
            # Simulate attention mechanism
            weight = round(random.uniform(0.1, 0.95), 3)
            attention_weights[word] = weight
        
        # Add context attention
        context_attention = {
            "temporal": round(random.uniform(0.3, 0.7), 3),
            "semantic": round(random.uniform(0.4, 0.8), 3),
            "structural": round(random.uniform(0.2, 0.6), 3)
        }
        
        return {
            "query": query,
            "word_attention": attention_weights,
            "context_attention": context_attention,
            "timestamp": datetime.now().isoformat()
        }
    
    def build_decision_tree(self, query: str, response: str) -> dict:
        """Build a decision tree representation of reasoning"""
        nodes = []
        depth = 0
        
        # Simulate decision nodes
        decision_points = [
            {"type": "intent_detection", "confidence": round(random.uniform(0.7, 0.99), 3)},
            {"type": "context_matching", "confidence": round(random.uniform(0.6, 0.95), 3)},
            {"type": "knowledge_retrieval", "confidence": round(random.uniform(0.75, 0.98), 3)},
            {"type": "reasoning_path", "confidence": round(random.uniform(0.8, 0.97), 3)}
        ]
        
        for node in decision_points:
            nodes.append({
                "id": len(nodes) + 1,
                "type": node["type"],
                "confidence": node["confidence"],
                "depth": depth,
                "children": random.randint(1, 3)
            })
        
        return {
            "query": query,
            "root_node": nodes[0] if nodes else None,
            "nodes": nodes,
            "tree_depth": len(nodes),
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_visualization_data(self, query: str, response: str) -> dict:
        """Generate complete visualization dataset"""
        return {
            "attention_map": self.generate_attention_map(query, []),
            "decision_tree": self.build_decision_tree(query, response),
            "activation_pattern": [round(random.uniform(0, 1), 4) for _ in range(128)],
            "graph_data": {
                "nodes": len(self.decision_graphs) + 1,
                "edges": random.randint(10, 100),
                "clusters": random.randint(3, 15)
            }
        }
    
    def save_visualization(self, query: str, response: str, metadata: dict = None):
        """Save visualization data to file"""
        viz_data = self.generate_visualization_data(query, response)
        
        if metadata:
            viz_data["metadata"] = metadata
        
        filename = f"visualization_{int(datetime.now().timestamp())}.json"
        filepath = self.visualization_log / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(viz_data, f, indent=2, ensure_ascii=False)
        
        self.decision_graphs.append(viz_data)
        return {"file": filename, "path": str(filepath)}

# Global instance
neural_viz = NeuralVisualizer()