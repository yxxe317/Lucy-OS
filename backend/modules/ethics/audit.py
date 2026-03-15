"""
Audit Module - Comprehensive logging and auditing
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class AuditModule:
    """
    Provides comprehensive auditing and logging capabilities
    """
    
    def __init__(self):
        self.audit_log = []
        self.alerts = []
        self.metrics = {}
        
    def log_event(self, event_type: str, user_id: str, action: str,
                   resource: str = None, details: Dict = None,
                   severity: str = 'info') -> str:
        """
        Log an audit event
        """
        import uuid
        event_id = str(uuid.uuid4())[:8]
        
        event = {
            'id': event_id,
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'details': details or {},
            'severity': severity
        }
        
        self.audit_log.append(event)
        
        # Trigger alert for high severity events
        if severity in ['critical', 'high']:
            self._create_alert(event)
        
        return event_id
    
    def _create_alert(self, event: Dict):
        """Create alert for high severity events"""
        alert = {
            'id': event['id'],
            'timestamp': event['timestamp'],
            'message': f"{event['severity'].upper()}: {event['action']} by {event['user_id']}",
            'event': event,
            'acknowledged': False
        }
        self.alerts.append(alert)
    
    def get_events(self, user_id: str = None, event_type: str = None,
                    start_time: datetime = None, end_time: datetime = None,
                    limit: int = 100) -> List[Dict]:
        """
        Get filtered audit events
        """
        filtered = self.audit_log
        
        if user_id:
            filtered = [e for e in filtered if e['user_id'] == user_id]
        if event_type:
            filtered = [e for e in filtered if e['event_type'] == event_type]
        if start_time:
            filtered = [e for e in filtered if datetime.fromisoformat(e['timestamp']) >= start_time]
        if end_time:
            filtered = [e for e in filtered if datetime.fromisoformat(e['timestamp']) <= end_time]
        
        return filtered[-limit:]
    
    def get_alerts(self, acknowledged: bool = None) -> List[Dict]:
        """
        Get alerts
        """
        if acknowledged is None:
            return self.alerts
        return [a for a in self.alerts if a['acknowledged'] == acknowledged]
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Acknowledge an alert
        """
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                alert['acknowledged_at'] = datetime.now().isoformat()
                return True
        return False
    
    def get_statistics(self, days: int = 7) -> Dict:
        """
        Get audit statistics
        """
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_events = [e for e in self.audit_log 
                        if datetime.fromisoformat(e['timestamp']) >= cutoff]
        
        # Count by event type
        event_types = {}
        for event in recent_events:
            etype = event['event_type']
            event_types[etype] = event_types.get(etype, 0) + 1
        
        # Count by severity
        severity_counts = {}
        for event in recent_events:
            sev = event['severity']
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        # Count by user
        user_counts = {}
        for event in recent_events:
            user = event['user_id']
            user_counts[user] = user_counts.get(user, 0) + 1
        
        return {
            'total_events': len(recent_events),
            'unique_users': len(user_counts),
            'event_types': event_types,
            'severity_counts': severity_counts,
            'top_users': sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'alerts_count': len([a for a in self.alerts if not a['acknowledged']])
        }
    
    def export_log(self, format: str = 'json') -> str:
        """
        Export audit log
        """
        if format == 'json':
            return json.dumps(self.audit_log, indent=2)
        elif format == 'csv':
            # Simple CSV export
            lines = ['timestamp,event_type,user_id,action,resource,severity']
            for event in self.audit_log:
                lines.append(f"{event['timestamp']},{event['event_type']},{event['user_id']},"
                           f"{event['action']},{event.get('resource','')},{event['severity']}")
            return '\n'.join(lines)
        else:
            return str(self.audit_log)
    
    def clear_old_events(self, days: int = 90):
        """
        Clear events older than specified days
        """
        cutoff = datetime.now() - timedelta(days=days)
        self.audit_log = [e for e in self.audit_log 
                         if datetime.fromisoformat(e['timestamp']) >= cutoff]
    
    def search_events(self, query: str) -> List[Dict]:
        """
        Search events by content
        """
        query_lower = query.lower()
        results = []
        
        for event in self.audit_log:
            # Search in string fields
            if (query_lower in event['user_id'].lower() or
                query_lower in event['action'].lower() or
                (event.get('resource') and query_lower in event['resource'].lower())):
                results.append(event)
                continue
            
            # Search in details
            for key, value in event.get('details', {}).items():
                if query_lower in str(key).lower() or query_lower in str(value).lower():
                    results.append(event)
                    break
        
        return results[-50:]  # Limit results