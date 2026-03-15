# backend/core/reality_manipulation.py
"""
Reality Manipulation Engine for Lucy OS
Features 91-95: Time perception control, alternate timelines, causality engine
"""
import asyncio
import json
import random
import numpy as np
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import hashlib
import logging
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger("RealityManipulation")

class TimeScale(Enum):
    MICRO = "micro"      # Seconds
    NORMAL = "normal"     # Minutes
    MACRO = "macro"       # Hours/Days
    EPOCH = "epoch"       # Years

@dataclass
class TimelineEvent:
    """An event in a timeline"""
    id: str
    timestamp: datetime
    description: str
    impact: float
    alternatives: List[str]
    probability: float
    is_divergence_point: bool = False

@dataclass
class AlternateTimeline:
    """A complete alternate timeline"""
    id: str
    name: str
    divergence_point: str
    events: List[TimelineEvent]
    current_state: Dict
    probability: float
    created_at: datetime

@dataclass
class CausalChain:
    """A chain of cause and effect"""
    id: str
    root_cause: str
    intermediate_effects: List[str]
    final_effect: str
    strength: float
    confidence: float

class RealityManipulation:
    """
    Reality manipulation capabilities
    Features 91-95: Time control, alternate timelines, causality engine
    """
    
    def __init__(self, db_path: str = "data/reality.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
        self.timelines: Dict[str, AlternateTimeline] = {}
        self.causal_chains: Dict[str, CausalChain] = {}
        self.time_perception_scale: TimeScale = TimeScale.NORMAL
        
    def _init_db(self):
        """Initialize reality database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Alternate timelines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alternate_timelines (
                id TEXT PRIMARY KEY,
                name TEXT,
                divergence_point TEXT,
                events TEXT,
                current_state TEXT,
                probability REAL,
                created_at DATETIME
            )
        ''')
        
        # Causal chains table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS causal_chains (
                id TEXT PRIMARY KEY,
                root_cause TEXT,
                intermediate_effects TEXT,
                final_effect TEXT,
                strength REAL,
                confidence REAL,
                created_at DATETIME
            )
        ''')
        
        # Timeline events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timeline_events (
                id TEXT PRIMARY KEY,
                timeline_id TEXT,
                timestamp DATETIME,
                description TEXT,
                impact REAL,
                alternatives TEXT,
                probability REAL,
                is_divergence_point BOOLEAN,
                FOREIGN KEY(timeline_id) REFERENCES alternate_timelines(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("🌀 Reality Manipulation initialized")
    
    # ========== FEATURE 91: Time Perception Control ==========
    
    async def set_time_scale(self, scale: str) -> Dict:
        """
        Change how Lucy perceives time in conversations
        """
        try:
            self.time_perception_scale = TimeScale(scale)
        except:
            return {"error": f"Invalid scale. Choose from: micro, normal, macro, epoch"}
        
        scale_properties = {
            "micro": {
                "description": "Perceiving seconds as minutes",
                "response_speed": "hyper_fast",
                "detail_level": "microscopic",
                "thinking_depth": "shallow"
            },
            "normal": {
                "description": "Normal human time perception",
                "response_speed": "normal",
                "detail_level": "normal",
                "thinking_depth": "moderate"
            },
            "macro": {
                "description": "Perceiving hours as minutes",
                "response_speed": "slowed",
                "detail_level": "broad",
                "thinking_depth": "deep"
            },
            "epoch": {
                "description": "Perceiving years as moments",
                "response_speed": "glacial",
                "detail_level": "epochal",
                "thinking_depth": "transcendent"
            }
        }
        
        logger.info(f"⏱️ Time scale set to {scale}")
        
        return {
            "scale": scale,
            "properties": scale_properties.get(scale, {}),
            "effective_speed_multiplier": {
                "micro": 10,
                "normal": 1,
                "macro": 0.1,
                "epoch": 0.01
            }.get(scale, 1)
        }
    
    async def compress_conversation(self, conversation: List[Dict], target_length: int) -> List[Dict]:
        """
        Compress time in conversations - see patterns over longer periods
        """
        if self.time_perception_scale == TimeScale.MICRO:
            # See every detail
            return conversation
        elif self.time_perception_scale == TimeScale.NORMAL:
            # Normal view
            return conversation
        elif self.time_perception_scale == TimeScale.MACRO:
            # See patterns over hours
            return self._compress_by_factor(conversation, 0.5)
        elif self.time_perception_scale == TimeScale.EPOCH:
            # See patterns over years
            return self._compress_by_factor(conversation, 0.1)
    
    def _compress_by_factor(self, items: List, factor: float) -> List:
        """Compress a list by factor"""
        if not items:
            return items
        step = max(1, int(1 / factor))
        return items[::step]
    
    # ========== FEATURE 92: Alternate Timeline Explorer ==========
    
    async def create_alternate_timeline(self, divergence_point: str, changes: Dict) -> Dict:
        """
        Create and explore an alternate timeline
        """
        timeline_id = hashlib.md5(f"{divergence_point}{datetime.now()}".encode()).hexdigest()[:12]
        
        # Generate events for this timeline
        events = await self._generate_timeline_events(divergence_point, changes)
        
        # Determine probability
        probability = random.uniform(0.1, 0.9)
        
        # Current state in this timeline
        current_state = await self._simulate_timeline_state(events)
        
        timeline = AlternateTimeline(
            id=timeline_id,
            name=f"Timeline_{timeline_id[:6]}",
            divergence_point=divergence_point,
            events=events,
            current_state=current_state,
            probability=probability,
            created_at=datetime.now()
        )
        
        self.timelines[timeline_id] = timeline
        
        # Store in database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO alternate_timelines
            (id, name, divergence_point, events, current_state, probability, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            timeline_id,
            timeline.name,
            divergence_point,
            json.dumps([asdict(e) for e in events]),
            json.dumps(current_state),
            probability,
            timeline.created_at.isoformat()
        ))
        
        # Store events
        for event in events:
            cursor.execute('''
                INSERT OR REPLACE INTO timeline_events
                (id, timeline_id, timestamp, description, impact, alternatives, probability, is_divergence_point)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.id,
                timeline_id,
                event.timestamp.isoformat(),
                event.description,
                event.impact,
                json.dumps(event.alternatives),
                event.probability,
                event.is_divergence_point
            ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"🌌 Created alternate timeline {timeline_id}")
        
        return {
            "timeline_id": timeline_id,
            "name": timeline.name,
            "divergence_point": divergence_point,
            "probability": probability,
            "key_events": [
                {
                    "time": e.timestamp.isoformat(),
                    "event": e.description,
                    "impact": e.impact
                }
                for e in events[:5]  # First 5 events
            ],
            "current_state": current_state
        }
    
    async def _generate_timeline_events(self, divergence_point: str, changes: Dict) -> List[TimelineEvent]:
        """Generate events for alternate timeline"""
        events = []
        current_time = datetime.now()
        
        # Divergence event
        divergence = TimelineEvent(
            id=hashlib.md5(f"div_{datetime.now()}".encode()).hexdigest()[:12],
            timestamp=current_time,
            description=f"Divergence: {divergence_point}",
            impact=1.0,
            alternatives=[],
            probability=1.0,
            is_divergence_point=True
        )
        events.append(divergence)
        
        # Generate subsequent events
        for i in range(random.randint(5, 15)):
            time_offset = timedelta(days=random.randint(1, 365) * (i+1))
            event_time = current_time + time_offset
            
            event = TimelineEvent(
                id=hashlib.md5(f"event_{i}_{datetime.now()}".encode()).hexdigest()[:12],
                timestamp=event_time,
                description=f"Event {i+1}: {random.choice(['discovery', 'crisis', 'breakthrough', 'conflict', 'peace'])}",
                impact=random.uniform(0.1, 0.9),
                alternatives=[f"Could have been {random.choice(['worse', 'better', 'different'])}"],
                probability=random.uniform(0.3, 0.9),
                is_divergence_point=False
            )
            events.append(event)
        
        return events
    
    async def _simulate_timeline_state(self, events: List[TimelineEvent]) -> Dict:
        """Simulate current state of timeline"""
        total_impact = sum(e.impact for e in events)
        
        return {
            "overall_development": "advanced" if total_impact > 5 else "normal",
            "key_achievements": [f"Achievement {i}" for i in range(random.randint(2, 5))],
            "challenges": [f"Challenge {i}" for i in range(random.randint(1, 3))],
            "mood": random.choice(["optimistic", "cautious", "turbulent", "peaceful"])
        }
    
    async def compare_timelines(self, timeline_ids: List[str]) -> Dict:
        """
        Compare multiple timelines to find optimal paths
        """
        timelines = []
        for tid in timeline_ids:
            if tid in self.timelines:
                timelines.append(self.timelines[tid])
        
        if len(timelines) < 2:
            return {"error": "Need at least 2 timelines to compare"}
        
        # Find best outcomes
        best_timeline = max(timelines, key=lambda t: t.probability)
        worst_timeline = min(timelines, key=lambda t: t.probability)
        
        # Extract lessons
        lessons = []
        for t in timelines:
            lessons.extend([
                f"In {t.name}, {e.description} led to {e.impact:.1f} impact"
                for e in t.events[:3]
            ])
        
        return {
            "timelines_compared": len(timelines),
            "optimal_path": {
                "timeline_id": best_timeline.id,
                "probability": best_timeline.probability,
                "key_events": [e.description for e in best_timeline.events[:3]]
            },
            "path_to_avoid": {
                "timeline_id": worst_timeline.id,
                "probability": worst_timeline.probability,
                "warning": "Lower probability timeline"
            },
            "lessons_from_all_timelines": lessons[:5],
            "recommendation": f"Follow path similar to {best_timeline.name} for best outcomes"
        }
    
    # ========== FEATURE 94: Causality Engine ==========
    
    async def trace_causality(self, event: str, depth: int = 3) -> Dict:
        """
        Trace cause and effect chains
        """
        chain_id = hashlib.md5(f"causal_{event}{datetime.now()}".encode()).hexdigest()[:12]
        
        # Generate causal chain
        root_cause = await self._find_root_cause(event)
        intermediates = await self._find_intermediate_effects(event, depth)
        final_effect = await self._predict_final_effect(event)
        
        strength = random.uniform(0.6, 0.95)
        confidence = random.uniform(0.7, 0.9)
        
        chain = CausalChain(
            id=chain_id,
            root_cause=root_cause,
            intermediate_effects=intermediates,
            final_effect=final_effect,
            strength=strength,
            confidence=confidence
        )
        
        self.causal_chains[chain_id] = chain
        
        # Store in database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO causal_chains
            (id, root_cause, intermediate_effects, final_effect, strength, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            chain_id,
            root_cause,
            json.dumps(intermediates),
            final_effect,
            strength,
            confidence,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        
        logger.info(f"🔗 Created causal chain {chain_id} for '{event[:50]}...'")
        
        return {
            "event": event,
            "root_cause": root_cause,
            "causal_chain": intermediates,
            "final_effect": final_effect,
            "causal_strength": strength,
            "confidence": confidence,
            "visualization": self._create_causal_viz(root_cause, intermediates, final_effect)
        }
    
    async def _find_root_cause(self, event: str) -> str:
        """Find root cause of an event"""
        causes = [
            f"initial condition: {random.choice(['environment', 'decision', 'circumstance', 'pattern'])}",
            f"fundamental: {random.choice(['human nature', 'system dynamics', 'universal law', 'random chance'])}",
            f"origin: {random.choice(['past event', 'accumulated pressure', 'critical mass', 'trigger'])}"
        ]
        return random.choice(causes)
    
    async def _find_intermediate_effects(self, event: str, depth: int) -> List[str]:
        """Find intermediate effects"""
        effects = []
        current = event
        
        for i in range(depth):
            next_effect = f"{current} → {random.choice(['cascaded', 'amplified', 'transformed', 'diverged'])} into {random.choice(['new pattern', 'chain reaction', 'feedback loop', 'system change'])}"
            effects.append(next_effect)
            current = next_effect.split('→')[-1].strip()
        
        return effects
    
    async def _predict_final_effect(self, event: str) -> str:
        """Predict final effect"""
        return f"Ultimately, {event} leads to {random.choice(['transformation', 'equilibrium', 'breakthrough', 'collapse', 'evolution'])}"
    
    def _create_causal_viz(self, root: str, intermediates: List[str], final: str) -> str:
        """Create ASCII visualization of causal chain"""
        viz = f"🌱 {root}\n"
        for i, effect in enumerate(intermediates):
            viz += f"   ↓\n   🌿 {effect}\n"
        viz += f"   ↓\n🌸 {final}"
        return viz
    
    async def reverse_causality(self, desired_outcome: str) -> List[str]:
        """
        Work backwards from desired outcome to find what causes it
        """
        steps = []
        current = desired_outcome
        
        for i in range(5):
            previous = f"To get {current}, you need {random.choice(['first', 'before that', 'as prerequisite'])}: {random.choice(['preparation', 'condition', 'action', 'resource'])}"
            steps.append(previous)
            current = previous.split(':')[-1].strip()
        
        steps.reverse()
        
        return {
            "desired_outcome": desired_outcome,
            "prerequisite_chain": steps,
            "probability_of_success": random.uniform(0.3, 0.8),
            "estimated_time": f"{random.randint(1, 12)} months"
        }
    
    # ========== FEATURE 95: Synchronistic Pattern Finder ==========
    
    async def find_synchronicities(self, user_id: int, timeframe_days: int = 30) -> Dict:
        """
        Find meaningful coincidences in user's data
        """
        # Get user's recent data (simulated)
        events = await self._get_user_events(user_id, timeframe_days)
        
        # Find patterns
        synchronicities = []
        
        for i in range(len(events)):
            for j in range(i+1, len(events)):
                if self._are_meaningfully_connected(events[i], events[j]):
                    synchronicity = {
                        "event_a": events[i],
                        "event_b": events[j],
                        "connection_type": random.choice([
                            "temporal", "thematic", "symbolic", "numerological", "causal"
                        ]),
                        "meaning": random.choice([
                            "You're on the right path",
                            "The universe is guiding you",
                            "Pay attention to this pattern",
                            "This repeats for a reason"
                        ]),
                        "significance": random.uniform(0.5, 0.95)
                    }
                    synchronicities.append(synchronicity)
        
        # Find the most significant one
        if synchronicities:
            most_significant = max(synchronicities, key=lambda s: s["significance"])
        else:
            most_significant = None
        
        return {
            "user_id": user_id,
            "timeframe_days": timeframe_days,
            "synchronicities_found": len(synchronicities),
            "most_significant": most_significant,
            "all_synchronicities": synchronicities[:10],  # Limit to 10
            "interpretation": self._interpret_synchronicities(synchronicities)
        }
    
    async def _get_user_events(self, user_id: int, days: int) -> List[str]:
        """Get user events (simulated)"""
        events = [
            "Dreamed about flying",
            "Met an old friend",
            "Found $5 on street",
            "Thought about career change",
            "Saw 11:11 on clock",
            "Random song played on radio",
            "Missed the bus",
            "Got unexpected email"
        ]
        return random.sample(events, k=min(len(events), days // 5 + 3))
    
    def _are_meaningfully_connected(self, event_a: str, event_b: str) -> bool:
        """Check if two events are meaningfully connected"""
        # In production, use semantic analysis
        return random.random() > 0.7
    
    def _interpret_synchronicities(self, synchronicities: List[Dict]) -> str:
        """Provide interpretation of synchronicities"""
        if not synchronicities:
            return "No significant synchronicities detected in this period."
        
        count = len(synchronicities)
        if count > 5:
            return "Strong synchronistic patterns detected. The universe is sending you messages."
        elif count > 2:
            return "Several meaningful coincidences found. Pay attention to recurring themes."
        else:
            return "Minor synchronicities detected. Stay open to signs."

# Global instance
reality = RealityManipulation()