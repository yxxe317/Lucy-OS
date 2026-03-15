"""
Knowledge Graph - Entity-relationship storage and querying
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Set, Optional, Any, Tuple

class KnowledgeGraph:
    """
    Stores entities and their relationships
    """
    
    def __init__(self, path: str = "knowledge_graph.json"):
        self.path = path
        self.entities = {}  # id -> entity data
        self.relations = []  # list of (source, relation, target, strength)
        self.entity_types = set()
        self.relation_types = set()
        
        self.load()
    
    def add_entity(self, name: str, entity_type: str, 
                    properties: Dict = None) -> str:
        """
        Add an entity to the graph
        """
        entity_id = hashlib.md5(f"{name}{entity_type}".encode()).hexdigest()[:16]
        
        self.entities[entity_id] = {
            'id': entity_id,
            'name': name,
            'type': entity_type,
            'properties': properties or {},
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
        
        self.entity_types.add(entity_type)
        return entity_id
    
    def add_relation(self, source_id: str, relation: str, 
                      target_id: str, strength: float = 1.0,
                      properties: Dict = None):
        """
        Add a relationship between entities
        """
        self.relations.append({
            'source': source_id,
            'relation': relation,
            'target': target_id,
            'strength': strength,
            'properties': properties or {},
            'created': datetime.now().isoformat()
        })
        
        self.relation_types.add(relation)
    
    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """
        Get entity by ID
        """
        return self.entities.get(entity_id)
    
    def find_entity(self, name: str, entity_type: str = None) -> List[Dict]:
        """
        Find entities by name
        """
        results = []
        name_lower = name.lower()
        
        for entity in self.entities.values():
            if name_lower in entity['name'].lower():
                if entity_type is None or entity['type'] == entity_type:
                    results.append(entity)
        
        return results
    
    def query_relations(self, source_id: str = None, relation: str = None,
                         target_id: str = None) -> List[Dict]:
        """
        Query relationships
        """
        results = []
        
        for rel in self.relations:
            if source_id and rel['source'] != source_id:
                continue
            if relation and rel['relation'] != relation:
                continue
            if target_id and rel['target'] != target_id:
                continue
            results.append(rel)
        
        return results
    
    def get_connected(self, entity_id: str, max_depth: int = 2) -> Dict:
        """
        Get all entities connected to given entity
        """
        connected = {
            'entity': self.get_entity(entity_id),
            'incoming': [],
            'outgoing': [],
            'network': {}
        }
        
        # Find direct connections
        for rel in self.relations:
            if rel['source'] == entity_id:
                target = self.get_entity(rel['target'])
                if target:
                    connected['outgoing'].append({
                        'relation': rel['relation'],
                        'target': target,
                        'strength': rel['strength']
                    })
            
            if rel['target'] == entity_id:
                source = self.get_entity(rel['source'])
                if source:
                    connected['incoming'].append({
                        'relation': rel['relation'],
                        'source': source,
                        'strength': rel['strength']
                    })
        
        # Build network if depth > 1
        if max_depth > 1:
            network = {}
            for out in connected['outgoing']:
                target_id = out['target']['id']
                network[target_id] = self.get_connected(target_id, max_depth - 1)
            connected['network'] = network
        
        return connected
    
    def get_entity_types(self) -> List[str]:
        """Get all entity types"""
        return sorted(self.entity_types)
    
    def get_relation_types(self) -> List[str]:
        """Get all relation types"""
        return sorted(self.relation_types)
    
    def get_statistics(self) -> Dict:
        """Get graph statistics"""
        return {
            'entities': len(self.entities),
            'relations': len(self.relations),
            'entity_types': len(self.entity_types),
            'relation_types': len(self.relation_types),
            'avg_relations_per_entity': len(self.relations) / max(1, len(self.entities))
        }
    
    def save(self):
        """Save graph to file"""
        data = {
            'entities': self.entities,
            'relations': self.relations,
            'entity_types': list(self.entity_types),
            'relation_types': list(self.relation_types),
            'updated': datetime.now().isoformat()
        }
        
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load graph from file"""
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                self.entities = data.get('entities', {})
                self.relations = data.get('relations', [])
                self.entity_types = set(data.get('entity_types', []))
                self.relation_types = set(data.get('relation_types', []))
        except:
            # Initialize with some default knowledge
            self._init_default_knowledge()
    
    def _init_default_knowledge(self):
        """Initialize with basic knowledge"""
        # Add some default entities
        earth_id = self.add_entity("Earth", "planet", {"type": "terrestrial"})
        moon_id = self.add_entity("Moon", "moon", {"orbits": "Earth"})
        sun_id = self.add_entity("Sun", "star", {"type": "yellow dwarf"})
        
        self.add_relation(earth_id, "orbits", sun_id, 1.0)
        self.add_relation(moon_id, "orbits", earth_id, 1.0)
        
        # Add some countries
        usa_id = self.add_entity("USA", "country", {"capital": "Washington DC"})
        canada_id = self.add_entity("Canada", "country", {"capital": "Ottawa"})
        mexico_id = self.add_entity("Mexico", "country", {"capital": "Mexico City"})
        
        self.add_relation(usa_id, "borders", canada_id, 0.8)
        self.add_relation(usa_id, "borders", mexico_id, 0.8)