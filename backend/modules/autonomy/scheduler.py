"""
Scheduler - Time management and scheduling
"""

import random
import heapq
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta

class Scheduler:
    """
    Manages schedules and time-based events
    """
    
    def __init__(self):
        self.events = []  # Priority queue of events
        self.schedules = {}
        self.reminders = []
        self.event_counter = 0
        
    def add_event(self, name: str, event_time: datetime,
                   duration: int = 60, priority: int = 1,
                   callback: Callable = None) -> str:
        """
        Add a scheduled event
        """
        import uuid
        event_id = str(uuid.uuid4())[:8]
        
        event = {
            'id': event_id,
            'name': name,
            'time': event_time,
            'duration': duration,
            'priority': priority,
            'callback': callback,
            'status': 'scheduled',
            'created': datetime.now()
        }
        
        # Push to priority queue (earliest time first)
        heapq.heappush(self.events, (event_time, priority, self.event_counter, event))
        self.event_counter += 1
        
        return event_id
    
    def add_daily_event(self, name: str, hour: int, minute: int,
                         duration: int = 60, callback: Callable = None) -> str:
        """
        Add a daily recurring event
        """
        now = datetime.now()
        event_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if event_time < now:
            event_time += timedelta(days=1)
        
        return self.add_event(f"Daily: {name}", event_time, duration, callback=callback)
    
    def add_weekly_event(self, name: str, weekday: int, hour: int,
                          minute: int, callback: Callable = None) -> str:
        """
        Add a weekly recurring event
        """
        now = datetime.now()
        days_ahead = (weekday - now.weekday()) % 7
        event_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0) + timedelta(days=days_ahead)
        
        if event_time < now:
            event_time += timedelta(weeks=1)
        
        return self.add_event(f"Weekly: {name}", event_time, callback=callback)
    
    def add_reminder(self, message: str, remind_at: datetime) -> str:
        """
        Add a reminder
        """
        import uuid
        reminder_id = str(uuid.uuid4())[:8]
        
        reminder = {
            'id': reminder_id,
            'message': message,
            'time': remind_at,
            'triggered': False
        }
        
        self.reminders.append(reminder)
        return reminder_id
    
    def check_events(self) -> List[Dict]:
        """
        Check for due events
        """
        now = datetime.now()
        due_events = []
        
        # Check scheduled events
        while self.events and self.events[0][0] <= now:
            event_time, priority, counter, event = heapq.heappop(self.events)
            due_events.append(event)
            
            # Execute callback if exists
            if event['callback']:
                try:
                    event['callback']()
                except Exception as e:
                    print(f"Callback error for {event['name']}: {e}")
        
        # Check reminders
        for reminder in self.reminders:
            if not reminder['triggered'] and reminder['time'] <= now:
                due_events.append({
                    'id': reminder['id'],
                    'name': 'Reminder',
                    'message': reminder['message'],
                    'type': 'reminder'
                })
                reminder['triggered'] = True
        
        return due_events
    
    def get_upcoming_events(self, limit: int = 10) -> List[Dict]:
        """
        Get upcoming events
        """
        events = []
        for event_time, priority, counter, event in sorted(self.events)[:limit]:
            events.append({
                'id': event['id'],
                'name': event['name'],
                'time': event_time.isoformat(),
                'duration': event['duration'],
                'priority': priority
            })
        return events
    
    def get_today_schedule(self) -> List[Dict]:
        """
        Get today's schedule
        """
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        today_events = []
        for event_time, priority, counter, event in self.events:
            if today_start <= event_time < today_end:
                today_events.append({
                    'id': event['id'],
                    'name': event['name'],
                    'time': event_time.strftime('%H:%M'),
                    'duration': event['duration']
                })
        
        return sorted(today_events, key=lambda e: e['time'])
    
    def cancel_event(self, event_id: str) -> bool:
        """
        Cancel an event
        """
        # Rebuild heap without cancelled event
        new_events = []
        cancelled = False
        
        for item in self.events:
            event_time, priority, counter, event = item
            if event['id'] != event_id:
                new_events.append(item)
            else:
                cancelled = True
        
        self.events = new_events
        heapq.heapify(self.events)
        
        return cancelled
    
    def suggest_schedule(self, tasks: List[Dict], available_hours: List[tuple]) -> List[Dict]:
        """
        Suggest optimal schedule for tasks
        """
        # Sort tasks by priority and duration
        sorted_tasks = sorted(tasks, key=lambda t: (-t.get('priority', 1), t.get('duration', 60)))
        
        schedule = []
        time_slot_index = 0
        
        for task in sorted_tasks:
            if time_slot_index < len(available_hours):
                start_time, end_time = available_hours[time_slot_index]
                duration = task.get('duration', 60)
                
                # Check if task fits in current slot
                slot_duration = (end_time - start_time).seconds / 60
                
                if duration <= slot_duration:
                    schedule.append({
                        'task': task['name'],
                        'start': start_time,
                        'end': start_time + timedelta(minutes=duration),
                        'duration': duration
                    })
                    
                    # Update remaining slot time
                    new_start = start_time + timedelta(minutes=duration)
                    available_hours[time_slot_index] = (new_start, end_time)
                else:
                    time_slot_index += 1
        
        return schedule
    
    def get_free_time(self, date: datetime) -> List[tuple]:
        """
        Get free time slots for a given date
        """
        day_start = date.replace(hour=9, minute=0)  # 9 AM
        day_end = date.replace(hour=17, minute=0)   # 5 PM
        
        busy_slots = []
        for event_time, priority, counter, event in self.events:
            event_date = event_time.date()
            if event_date == date.date():
                event_end = event_time + timedelta(minutes=event['duration'])
                busy_slots.append((event_time, event_end))
        
        # Sort busy slots
        busy_slots.sort()
        
        # Find free slots
        free_slots = []
        current = day_start
        
        for start, end in busy_slots:
            if current < start:
                free_slots.append((current, start))
            current = max(current, end)
        
        if current < day_end:
            free_slots.append((current, day_end))
        
        return free_slots