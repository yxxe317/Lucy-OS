"""
Calendar Integration - Google Calendar events
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

class Calendar:
    """
    Calendar management (simulated)
    """
    
    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path
        self.events_file = "calendar_events.json"
        self.events = self._load_events()
    
    def _load_events(self) -> List[Dict]:
        """Load events from file"""
        if os.path.exists(self.events_file):
            try:
                with open(self.events_file, 'r') as f:
                    return json.load(f)
            except:
                return self._generate_sample_events()
        else:
            return self._generate_sample_events()
    
    def _save_events(self):
        """Save events to file"""
        with open(self.events_file, 'w') as f:
            json.dump(self.events, f, indent=2)
    
    def _generate_sample_events(self) -> List[Dict]:
        """Generate sample events"""
        today = datetime.now()
        
        return [
            {
                'id': '1',
                'title': 'Team Meeting',
                'start': (today.replace(hour=10, minute=0)).isoformat(),
                'end': (today.replace(hour=11, minute=0)).isoformat(),
                'location': 'Conference Room A',
                'description': 'Weekly team sync',
                'attendees': ['alice@example.com', 'bob@example.com']
            },
            {
                'id': '2',
                'title': 'Lunch with Client',
                'start': (today.replace(hour=12, minute=30)).isoformat(),
                'end': (today.replace(hour=13, minute=30)).isoformat(),
                'location': 'Cafe Downtown',
                'description': 'Discuss project requirements',
                'attendees': ['client@example.com']
            },
            {
                'id': '3',
                'title': 'Project Review',
                'start': (today.replace(hour=15, minute=0)).isoformat(),
                'end': (today.replace(hour=16, minute=0)).isoformat(),
                'location': 'Conference Room B',
                'description': 'Review Q2 milestones',
                'attendees': ['team@example.com']
            }
        ]
    
    def get_events(self, date: str = None, days: int = 7) -> List[Dict]:
        """
        Get events for a date range
        """
        if date:
            target_date = datetime.fromisoformat(date).date()
        else:
            target_date = datetime.now().date()
        
        end_date = target_date + timedelta(days=days)
        
        events = []
        for event in self.events:
            event_date = datetime.fromisoformat(event['start']).date()
            if target_date <= event_date <= end_date:
                events.append(event)
        
        return sorted(events, key=lambda x: x['start'])
    
    def add_event(self, title: str, start: str, end: str,
                   location: str = None, description: str = None,
                   attendees: List[str] = None) -> Dict:
        """
        Add a new event
        """
        import uuid
        
        event = {
            'id': str(uuid.uuid4())[:8],
            'title': title,
            'start': start,
            'end': end,
            'location': location or '',
            'description': description or '',
            'attendees': attendees or []
        }
        
        self.events.append(event)
        self._save_events()
        return event
    
    def update_event(self, event_id: str, updates: Dict) -> bool:
        """
        Update an existing event
        """
        for event in self.events:
            if event['id'] == event_id:
                event.update(updates)
                self._save_events()
                return True
        return False
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event
        """
        for i, event in enumerate(self.events):
            if event['id'] == event_id:
                del self.events[i]
                self._save_events()
                return True
        return False
    
    def get_upcoming(self, limit: int = 5) -> List[Dict]:
        """
        Get upcoming events
        """
        now = datetime.now().isoformat()
        upcoming = [e for e in self.events if e['start'] >= now]
        return sorted(upcoming, key=lambda x: x['start'])[:limit]
    
    def find_free_slots(self, date: str, duration_minutes: int = 60) -> List[Dict]:
        """
        Find free time slots on a given date
        """
        target_date = datetime.fromisoformat(date).date()
        day_events = self.get_events(date, days=1)
        
        # Sort events by start time
        day_events.sort(key=lambda x: x['start'])
        
        # Business hours 9 AM - 5 PM
        work_start = datetime.combine(target_date, datetime.min.time().replace(hour=9))
        work_end = datetime.combine(target_date, datetime.min.time().replace(hour=17))
        
        slots = []
        current = work_start
        
        for event in day_events:
            event_start = datetime.fromisoformat(event['start'])
            event_end = datetime.fromisoformat(event['end'])
            
            # Check if there's a gap
            if (event_start - current).total_seconds() / 60 >= duration_minutes:
                slots.append({
                    'start': current.isoformat(),
                    'end': event_start.isoformat(),
                    'duration': int((event_start - current).total_seconds() / 60)
                })
            
            current = max(current, event_end)
        
        # Check after last event
        if (work_end - current).total_seconds() / 60 >= duration_minutes:
            slots.append({
                'start': current.isoformat(),
                'end': work_end.isoformat(),
                'duration': int((work_end - current).total_seconds() / 60)
            })
        
        return slots