"""
Memory Palace - Spatial memory visualization and organization
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

class MemoryPalace:
    """
    Organizes memories using spatial metaphor (Method of Loci)
    """
    
    def __init__(self):
        self.rooms = {}  # Memory rooms/spaces
        self.locations = {}  # Specific locations within rooms
        self.current_room = "entrance"
        
        # Initialize with default palace structure
        self._init_palace()
    
    def _init_palace(self):
        """Initialize default memory palace"""
        self.rooms = {
            "entrance": {
                "name": "Main Entrance",
                "description": "The gateway to knowledge",
                "locations": ["gate", "hall", "garden"],
                "memories": []
            },
            "library": {
                "name": "Grand Library",
                "description": "Facts and general knowledge",
                "locations": ["shelves", "reading_room", "archive"],
                "memories": []
            },
            "hall_of_faces": {
                "name": "Hall of Faces",
                "description": "People and relationships",
                "locations": ["portraits", "meeting_room", "memory_wall"],
                "memories": []
            },
            "time_corridor": {
                "name": "Time Corridor",
                "description": "Episodic memories",
                "locations": ["past_room", "present_room", "future_room"],
                "memories": []
            },
            "emotion_garden": {
                "name": "Emotion Garden",
                "description": "Emotional memories",
                "locations": ["joy_fountain", "reflection_pond", "meditation_grove"],
                "memories": []
            },
            "skill_tower": {
                "name": "Skill Tower",
                "description": "Procedural memories",
                "locations": ["practice_room", "master_chamber", "innovation_lab"],
                "memories": []
            },
            "quantum_chamber": {
                "name": "Quantum Chamber",
                "description": "Abstract concepts and quantum thoughts",
                "locations": ["superposition", "entanglement", "observation"],
                "memories": []
            }
        }
        
        # Initialize locations
        for room_name, room in self.rooms.items():
            for loc in room["locations"]:
                loc_id = f"{room_name}_{loc}"
                self.locations[loc_id] = {
                    "room": room_name,
                    "name": loc.replace("_", " ").title(),
                    "memories": []
                }
    
    def place_memory(self, memory_id: str, memory_data: Dict, 
                      room: Optional[str] = None,
                      location: Optional[str] = None) -> Tuple[str, str]:
        """
        Place a memory in the palace
        Returns (room, location)
        """
        # Determine best room based on memory type
        if room is None:
            room = self._suggest_room(memory_data)
        
        # Determine best location in room
        if location is None:
            location = self._suggest_location(room, memory_data)
        
        loc_id = f"{room}_{location}"
        
        if loc_id in self.locations:
            self.locations[loc_id]["memories"].append({
                'id': memory_id,
                'data': memory_data,
                'placed_at': datetime.now().isoformat()
            })
            
            # Also add to room's memory list
            if room in self.rooms:
                self.rooms[room]["memories"].append(memory_id)
        
        return room, location
    
    def recall_from_location(self, room: str, location: str) -> List[Dict]:
        """
        Recall memories from specific location
        """
        loc_id = f"{room}_{location}"
        if loc_id in self.locations:
            return self.locations[loc_id]["memories"]
        return []
    
    def recall_from_room(self, room: str) -> List[Dict]:
        """
        Recall all memories from a room
        """
        memories = []
        for loc_id, loc in self.locations.items():
            if loc["room"] == room:
                memories.extend(loc["memories"])
        return memories
    
    def walk_through(self, room: Optional[str] = None) -> List[Dict]:
        """
        Guided tour through memory palace
        """
        if room:
            return self.recall_from_room(room)
        
        # Tour through all rooms
        all_memories = []
        for room_name in self.rooms:
            all_memories.extend(self.recall_from_room(room_name))
        return all_memories
    
    def _suggest_room(self, memory_data: Dict) -> str:
        """
        Suggest best room based on memory type
        """
        memory_type = memory_data.get('type', 'general')
        
        room_map = {
            'fact': 'library',
            'knowledge': 'library',
            'person': 'hall_of_faces',
            'relationship': 'hall_of_faces',
            'conversation': 'time_corridor',
            'experience': 'time_corridor',
            'emotion': 'emotion_garden',
            'feeling': 'emotion_garden',
            'skill': 'skill_tower',
            'procedure': 'skill_tower',
            'quantum': 'quantum_chamber',
            'abstract': 'quantum_chamber'
        }
        
        return room_map.get(memory_type, 'entrance')
    
    def _suggest_location(self, room: str, memory_data: Dict) -> str:
        """
        Suggest best location within room
        """
        room_info = self.rooms.get(room, {})
        locations = room_info.get('locations', [])
        
        if not locations:
            return "default"
        
        # Simple round-robin for now
        import hashlib
        memory_hash = int(hashlib.md5(str(memory_data).encode()).hexdigest(), 16)
        return locations[memory_hash % len(locations)]
    
    def get_palace_map(self) -> Dict:
        """
        Get full palace structure
        """
        return {
            'rooms': self.rooms,
            'locations': {
                loc_id: {
                    'room': loc['room'],
                    'name': loc['name'],
                    'memory_count': len(loc['memories'])
                }
                for loc_id, loc in self.locations.items()
            }
        }
    
    def visualize(self) -> str:
        """
        Create ASCII visualization of memory palace
        """
        palace_map = self.get_palace_map()
        
        output = "\n" + "="*60 + "\n"
        output += "                MEMORY PALACE MAP\n"
        output += "="*60 + "\n\n"
        
        for room_name, room in self.rooms.items():
            # Room header
            output += f"🏛️  {room['name']}\n"
            output += f"   {room['description']}\n"
            output += f"   Locations: {', '.join(l.replace('_', ' ') for l in room['locations'])}\n"
            
            # Memory count
            mem_count = len(room['memories'])
            output += f"   📚 Memories: {mem_count}\n"
            
            # Show some memories if any
            if mem_count > 0:
                output += f"   Recent: "
                recent = room['memories'][-3:]
                output += ", ".join([m[:20] + "..." for m in recent]) + "\n"
            
            output += "\n"
        
        output += "="*60
        return output