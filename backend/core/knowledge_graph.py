"""
Knowledge Graph Auto-Builder - Dynamic knowledge structure construction and maintenance
"""
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
import json

class KnowledgeGraphAutoBuilder:
    def __init__(self):
        self.kg_path = Path("data/knowledge_graph")
        self.kg_path.mkdir(exist_ok=True)
        self.nodes: Dict[str, Dict] = {}
        self.edges: List[Dict] = []
        self.auto_rules: List[Dict] = []
        self.concept_clusters: Dict[str, List[str]] = {}
        self.relation_types: Dict[str, List[str]] = {}
    
    def register_node(self, node_id: str, properties: Dict = None) -> dict:
        """Register a new node in the knowledge graph"""
        node = {
            "id": node_id,
            "properties": properties or {},
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "connections": []
        }
        self.nodes[node_id] = node
        return {"registered": node_id, "total_nodes": len(self.nodes)}
    
    def auto_discover_relations(self, node_id: str, context: Dict = None) -> dict:
        """Automatically discover relations for a node based on context"""
        if node_id not in self.nodes:
            return {"error": f"Node '{node_id}' not found"}
        
        node = self.nodes[node_id]
        context = context or {}
        
        # Apply auto-discovery rules
        discovered = []
        for rule in self.auto_rules:
            if rule["trigger"](node, context):
                result = rule["action"](node, context)
                discovered.extend(result)
        
        # Update node with discovered relations
        for discovery in discovered:
            if discovery["relation"] not in node["connections"]:
                node["connections"].append(discovery["relation"])
        
        return {
            "node": node_id,
            "discovered_relations": discovered,
            "total_connections": len(node["connections"]),
            "timestamp": datetime.now().isoformat()
        }
    
    def cluster_concepts(self, min_cluster_size: int = 3) -> dict:
        """Auto-cluster related concepts"""
        if not self.nodes:
            return {"error": "No nodes to cluster"}
        
        # Extract all properties from nodes
        all_properties = []
        for node in self.nodes.values():
            props = node.get("properties", {})
            all_properties.extend(props.keys())
        
        # Group by common prefixes/suffixes
        clusters = {}
        for prop in all_properties:
            # Create cluster keys based on patterns
            prefix = prop.split("_")[0] if "_" in prop else prop[:3]
            if prefix not in clusters:
                clusters[prefix] = []
            clusters[prefix].append(prop)
        
        # Filter by minimum size
        valid_clusters = {k: v for k, v in clusters.items() if len(v) >= min_cluster_size}
        
        return {
            "clusters": valid_clusters,
            "total_clusters": len(valid_clusters),
            "total_concepts": len(all_properties),
            "timestamp": datetime.now().isoformat()
        }
    
    def auto_enrich_node(self, node_id: str, source: str = "internal") -> dict:
        """Automatically enrich a node with related information"""
        if node_id not in self.nodes:
            return {"error": f"Node '{node_id}' not found"}
        
        node = self.nodes[node_id]
        enrichment = {
            "node": node_id,
            "source": source,
            "enrichments": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Apply enrichment rules
        for rule in self.auto_rules:
            if rule["enrichment"](node):
                result = rule["enrichment"](node)
                enrichment["enrichments"].append(result)
        
        # Update node
        node["modified"] = datetime.now().isoformat()
        
        return enrichment
    
    def create_relation(self, source: str, target: str, relation_type: str, 
                       properties: Dict = None) -> dict:
        """Create a relation between nodes"""
        if source not in self.nodes:
            return {"error": f"Source node '{source}' not found"}
        if target not in self.nodes:
            return {"error": f"Target node '{target}' not found"}
        
        relation = {
            "source": source,
            "target": target,
            "relation_type": relation_type,
            "properties": properties or {},
            "created": datetime.now().isoformat()
        }
        self.edges.append(relation)
        
        # Update node connections
        if "connections" not in self.nodes[source]:
            self.nodes[source]["connections"] = []
        if "connections" not in self.nodes[target]:
            self.nodes[target]["connections"] = []
        
        self.nodes[source]["connections"].append(target)
        self.nodes[target]["connections"].append(source)
        
        return {
            "relation": relation,
            "total_edges": len(self.edges),
            "timestamp": datetime.now().isoformat()
        }
    
    def auto_suggest_relations(self, node_id: str) -> List[Dict]:
        """Auto-suggest potential relations for a node"""
        if node_id not in self.nodes:
            return []
        
        node = self.nodes[node_id]
        suggestions = []
        
        # Suggest relations based on node properties
        properties = node.get("properties", {})
        
        # Check for common relation patterns
        relation_patterns = [
            ("related_to", "semantic similarity"),
            ("instance_of", "hierarchical relationship"),
            ("part_of", "composition relationship"),
            ("causes", "causal relationship"),
            ("located_in", "spatial relationship")
        ]
        
        for relation_type, pattern_desc in relation_patterns:
            # Simple heuristic: suggest if property matches pattern
            if any(pattern_desc.lower() in str(properties).lower() 
                   for pattern_desc in [pattern_desc]):
                suggestions.append({
                    "node": node_id,
                    "relation": relation_type,
                    "confidence": random.uniform(0.6, 0.9),
                    "pattern": pattern_desc
                })
        
        return suggestions
    
    def auto_merge_nodes(self, node1: str, node2: str, 
                        confidence_threshold: float = 0.7) -> dict:
        """Automatically merge similar nodes"""
        if node1 not in self.nodes or node2 not in self.nodes:
            return {"error": "One or both nodes not found"}
        
        node1_data = self.nodes[node1]
        node2_data = self.nodes[node2]
        
        # Calculate similarity
        props1 = set(node1_data.get("properties", {}).keys())
        props2 = set(node2_data.get("properties", {}).keys())
        
        if not props1 or not props2:
            similarity = 0.5
        else:
            intersection = props1 & props2
            union = props1 | props2
            similarity = len(intersection) / len(union) if union else 0
        
        if similarity >= confidence_threshold:
            # Merge nodes
            merged = {
                "id": f"{node1}_merged_{node2}",
                "properties": {**node1_data.get("properties", {}), 
                             **node2_data.get("properties", {})},
                "merged_from": [node1, node2],
                "merged_at": datetime.now().isoformat()
            }
            
            self.nodes[merged["id"]] = merged
            
            # Update connections
            all_connections = set(node1_data.get("connections", []) + 
                                node2_data.get("connections", []))
            for conn in all_connections:
                if conn not in self.nodes:
                    continue
                if "connections" not in self.nodes[conn]:
                    self.nodes[conn]["connections"] = []
                self.nodes[conn]["connections"].append(merged["id"])
            
            return {
                "merged": merged,
                "similarity": similarity,
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "nodes": [node1, node2],
            "similarity": similarity,
            "threshold": confidence_threshold,
            "merged": False,
            "timestamp": datetime.now().isoformat()
        }
    
    def auto_restructure(self) -> dict:
        """Auto-restructure the knowledge graph"""
        restructure = {
            "before": {
                "nodes": len(self.nodes),
                "edges": len(self.edges),
                "clusters": len(self.concept_clusters)
            },
            "actions": [],
            "after": {}
        }
        
        # Action 1: Cluster similar nodes
        clustering_result = self.cluster_concepts()
        restructure["actions"].append({
            "action": "clustering",
            "result": clustering_result
        })
        
        # Action 2: Suggest and create missing relations
        suggestions = []
        for node_id in list(self.nodes.keys())[:5]:  # Limit for performance
            suggestions.extend(self.auto_suggest_relations(node_id))
        
        created = 0
        for suggestion in suggestions[:10]:  # Limit suggestions
            if random.random() < 0.3:  # 30% chance to create
                self.create_relation(
                    suggestion["node"],
                    random.choice(list(self.nodes.keys())),
                    suggestion["relation"]
                )
                created += 1
        
        restructure["actions"].append({
            "action": "relation_suggestions",
            "suggested": len(suggestions),
            "created": created
        })
        
        # Update after state
        restructure["after"] = {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "clusters": len(self.concept_clusters)
        }
        
        return restructure
    
    def register_auto_rule(self, trigger: callable, action: callable, 
                          name: str = None) -> dict:
        """Register an auto-rule for the knowledge graph"""
        rule = {
            "name": name or f"rule_{len(self.auto_rules)}",
            "trigger": trigger,
            "action": action,
            "created": datetime.now().isoformat()
        }
        self.auto_rules.append(rule)
        return rule
    
    def export_knowledge_graph(self) -> str:
        """Export the knowledge graph to JSON"""
        data = {
            "nodes": self.nodes,
            "edges": self.edges,
            "clusters": self.concept_clusters,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.kg_path / "knowledge_graph.json", 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return f"Exported knowledge graph with {len(self.nodes)} nodes and {len(self.edges)} edges"

# Global instance
knowledge_graph = KnowledgeGraphAutoBuilder()