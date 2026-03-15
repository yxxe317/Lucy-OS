import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import random

logger = logging.getLogger("LucyAnalytics")

class SecurityAnalytics:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "security"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.alerts_file = self.data_dir / "alerts.json"
        self.metrics_file = self.data_dir / "metrics.json"
        self._init_data()
        logger.info("📊 Security Analytics Initialized")
    
    def _init_data(self):
        """Initialize data files"""
        if not self.alerts_file.exists():
            self._save_alerts([])
        if not self.metrics_file.exists():
            self._save_metrics(self._generate_sample_metrics())
    
    def _save_alerts(self, alerts: List):
        with open(self.alerts_file, 'w') as f:
            json.dump(alerts, f, indent=2)
    
    def _load_alerts(self) -> List:
        try:
            with open(self.alerts_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_metrics(self, metrics: Dict):
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
    
    def _load_metrics(self) -> Dict:
        try:
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        except:
            return self._generate_sample_metrics()
    
    def _generate_sample_metrics(self) -> Dict:
        """Generate sample metrics for dashboard demo"""
        now = datetime.now()
        return {
            "risk_score": random.randint(10, 40),
            "alerts_24h": random.randint(0, 15),
            "logs_processed": random.randint(1000, 5000),
            "threats_blocked": random.randint(5, 50),
            "compliance_score": random.randint(85, 100),
            "timeline": [
                {"date": (now - timedelta(days=i)).strftime("%Y-%m-%d"), "risk": random.randint(10, 50)}
                for i in range(7, 0, -1)
            ]
        }
    
    def get_dashboard_data(self) -> Dict:
        """Get main dashboard metrics"""
        metrics = self._load_metrics()
        alerts = self._load_alerts()
        
        return {
            "success": True,
            "risk_score": metrics["risk_score"],
            "alerts_total": len(alerts),
            "alerts_unresolved": len([a for a in alerts if a["status"] == "open"]),
            "logs_processed": metrics["logs_processed"],
            "threats_blocked": metrics["threats_blocked"],
            "compliance_score": metrics["compliance_score"],
            "timeline": metrics["timeline"],
            "last_updated": datetime.now().isoformat()
        }
    
    def create_alert(self, severity: str, description: str, source: str = "manual") -> Dict:
        """Create a security alert"""
        alerts = self._load_alerts()
        alert = {
            "id": len(alerts) + 1,
            "severity": severity,
            "description": description,
            "source": source,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "resolved_at": None
        }
        alerts.insert(0, alert)
        self._save_alerts(alerts)
        
        # Update metrics
        metrics = self._load_metrics()
        metrics["alerts_24h"] += 1
        if severity == "critical":
            metrics["risk_score"] = min(100, metrics["risk_score"] + 10)
        self._save_metrics(metrics)
        
        return {"success": True, "alert_id": alert["id"]}
    
    def resolve_alert(self, alert_id: int) -> Dict:
        """Resolve a security alert"""
        alerts = self._load_alerts()
        for alert in alerts:
            if alert["id"] == alert_id:
                alert["status"] = "resolved"
                alert["resolved_at"] = datetime.now().isoformat()
                break
        
        self._save_alerts(alerts)
        return {"success": True}
    
    def get_alerts(self, limit: int = 20) -> Dict:
        """Get recent alerts"""
        alerts = self._load_alerts()
        return {"success": True, "alerts": alerts[:limit]}
    
    def get_compliance_report(self) -> Dict:
        """Generate compliance checklist (NIST/ISO inspired)"""
        controls = [
            {"id": "AC-1", "name": "Access Control Policy", "status": "implemented"},
            {"id": "AC-2", "name": "Account Management", "status": "implemented"},
            {"id": "AU-1", "name": "Audit & Accountability", "status": "partial"},
            {"id": "IR-1", "name": "Incident Response Plan", "status": "implemented"},
            {"id": "SC-1", "name": "System & Communications Protection", "status": "implemented"},
            {"id": "SI-1", "name": "System & Information Integrity", "status": "partial"},
        ]
        
        implemented = sum(1 for c in controls if c["status"] == "implemented")
        score = int((implemented / len(controls)) * 100)
        
        return {
            "success": True,
            "framework": "NIST SP 800-53",
            "score": score,
            "controls": controls,
            "generated_at": datetime.now().isoformat()
        }
    
    def correlate_logs(self, log_events: List[str]) -> Dict:
        """Find correlated events (simple pattern matching)"""
        correlations = []
        
        # Simple correlation: multiple failed logins from same IP
        ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        ips = {}
        
        for event in log_events:
            import re
            matches = re.findall(ip_pattern, event)
            for ip in matches:
                ips[ip] = ips.get(ip, 0) + 1
        
        for ip, count in ips.items():
            if count >= 3:
                correlations.append({
                    "type": "brute_force_attempt",
                    "indicator": f"IP {ip}",
                    "occurrences": count,
                    "recommendation": "Block IP and investigate"
                })
        
        return {
            "success": True,
            "correlations_found": len(correlations),
            "correlations": correlations
        }

security_analytics = SecurityAnalytics()