import logging
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

logger = logging.getLogger("LucySOC")

class SOCSimulation:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "soc"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.scenarios_file = self.data_dir / "scenarios.json"
        self.incidents_file = self.data_dir / "incidents.json"
        self.certifications_file = self.data_dir / "certifications.json"
        self._init_data()
        logger.info("🎯 SOC Simulation Initialized")
    
    def _init_data(self):
        """Initialize data files"""
        if not self.scenarios_file.exists():
            self._save_scenarios(self._generate_scenarios())
        if not self.incidents_file.exists():
            self._save_incidents([])
        if not self.certifications_file.exists():
            self._save_certifications({})
    
    def _save_scenarios(self, scenarios: List):
        with open(self.scenarios_file, 'w') as f:
            json.dump(scenarios, f, indent=2)
    
    def _load_scenarios(self) -> List:
        try:
            with open(self.scenarios_file, 'r') as f:
                return json.load(f)
        except:
            return self._generate_scenarios()
    
    def _save_incidents(self, incidents: List):
        with open(self.incidents_file, 'w') as f:
            json.dump(incidents, f, indent=2)
    
    def _load_incidents(self) -> List:
        try:
            with open(self.incidents_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_certifications(self, certs: Dict):
        with open(self.certifications_file, 'w') as f:
            json.dump(certs, f, indent=2)
    
    def _load_certifications(self) -> Dict:
        try:
            with open(self.certifications_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _generate_scenarios(self) -> List:
        """Generate pre-built SOC training scenarios"""
        return [
            {
                "id": 1,
                "name": "Phishing Campaign",
                "difficulty": "beginner",
                "description": "Multiple employees report suspicious emails with malicious attachments",
                "objectives": [
                    "Identify phishing indicators",
                    "Contain affected systems",
                    "Document incident timeline",
                    "Send awareness notification"
                ],
                "mitre_techniques": ["T1566.001", "T1204.002"],
                "duration_minutes": 30,
                "roles_required": ["analyst", "responder"]
            },
            {
                "id": 2,
                "name": "Ransomware Detection",
                "difficulty": "intermediate",
                "description": "SIEM alerts show encrypted files and ransom notes on multiple workstations",
                "objectives": [
                    "Identify patient zero",
                    "Isolate infected systems",
                    "Determine ransomware variant",
                    "Initiate recovery procedures"
                ],
                "mitre_techniques": ["T1486", "T1490"],
                "duration_minutes": 60,
                "roles_required": ["analyst", "responder", "manager"]
            },
            {
                "id": 3,
                "name": "Insider Threat",
                "difficulty": "advanced",
                "description": "Unusual data access patterns detected from privileged user account",
                "objectives": [
                    "Analyze access logs",
                    "Interview stakeholders",
                    "Assess data exfiltration risk",
                    "Recommend containment actions"
                ],
                "mitre_techniques": ["T1078", "T1530"],
                "duration_minutes": 90,
                "roles_required": ["analyst", "responder", "manager", "legal"]
            },
            {
                "id": 4,
                "name": "DDoS Attack",
                "difficulty": "intermediate",
                "description": "Web services experiencing severe performance degradation from traffic surge",
                "objectives": [
                    "Confirm DDoS vs legitimate traffic",
                    "Implement traffic filtering",
                    "Coordinate with ISP",
                    "Document attack vectors"
                ],
                "mitre_techniques": ["T1498"],
                "duration_minutes": 45,
                "roles_required": ["analyst", "responder"]
            },
            {
                "id": 5,
                "name": "Supply Chain Compromise",
                "difficulty": "advanced",
                "description": "Third-party vendor reports breach that may affect your organization",
                "objectives": [
                    "Assess vendor relationship impact",
                    "Scan for IOCs",
                    "Review access permissions",
                    "Update vendor risk assessment"
                ],
                "mitre_techniques": ["T1199", "T1071"],
                "duration_minutes": 120,
                "roles_required": ["analyst", "responder", "manager"]
            }
        ]
    
    def get_dashboard_metrics(self) -> Dict:
        """Get SOC dashboard metrics"""
        incidents = self._load_incidents()
        active = len([i for i in incidents if i.get("status") == "active"])
        resolved = len([i for i in incidents if i.get("status") == "resolved"])
        
        return {
            "success": True,
            "active_incidents": active,
            "resolved_incidents": resolved,
            "total_scenarios": len(self._load_scenarios()),
            "mttr_minutes": random.randint(15, 120),  # Mean time to resolve
            "detection_rate": random.randint(85, 99),
            "team_readiness": random.randint(70, 100),
            "last_updated": datetime.now().isoformat()
        }
    
    def start_scenario(self, scenario_id: int, team_members: List[str]) -> Dict:
        """Start a new SOC simulation scenario"""
        scenarios = self._load_scenarios()
        scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
        
        if not scenario:
            return {"success": False, "error": "Scenario not found"}
        
        incident = {
            "id": len(self._load_incidents()) + 1,
            "scenario_id": scenario_id,
            "scenario_name": scenario["name"],
            "status": "active",
            "team_members": team_members,
            "role_assignments": {},
            "timeline": [],
            "actions_taken": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "score": 0,
            "feedback": []
        }
        
        incidents = self._load_incidents()
        incidents.append(incident)
        self._save_incidents(incidents)
        
        return {"success": True, "incident_id": incident["id"], "scenario": scenario}
    
    def add_timeline_event(self, incident_id: int, event: str, timestamp: str = None) -> Dict:
        """Add event to incident timeline"""
        incidents = self._load_incidents()
        for incident in incidents:
            if incident["id"] == incident_id:
                incident["timeline"].append({
                    "event": event,
                    "timestamp": timestamp or datetime.now().isoformat()
                })
                break
        
        self._save_incidents(incidents)
        return {"success": True}
    
    def take_action(self, incident_id: int, action: str, role: str) -> Dict:
        """Record action taken during incident"""
        incidents = self._load_incidents()
        for incident in incidents:
            if incident["id"] == incident_id:
                incident["actions_taken"].append({
                    "action": action,
                    "role": role,
                    "timestamp": datetime.now().isoformat()
                })
                break
        
        self._save_incidents(incidents)
        return {"success": True}
    
    def complete_incident(self, incident_id: int, score: int, feedback: List[str]) -> Dict:
        """Complete incident and generate after-action report"""
        incidents = self._load_incidents()
        for incident in incidents:
            if incident["id"] == incident_id:
                incident["status"] = "resolved"
                incident["completed_at"] = datetime.now().isoformat()
                incident["score"] = score
                incident["feedback"] = feedback
                break
        
        self._save_incidents(incidents)
        
        # Update certifications
        certs = self._load_certifications()
        for member in incident.get("team_members", []):
            if member not in certs:
                certs[member] = {"scenarios_completed": 0, "average_score": 0}
            certs[member]["scenarios_completed"] += 1
            certs[member]["average_score"] = int(
                (certs[member]["average_score"] + score) / 2
            )
        self._save_certifications(certs)
        
        return {"success": True, "report": self._generate_after_action_report(incident)}
    
    def _generate_after_action_report(self, incident: Dict) -> Dict:
        """Generate after-action report"""
        return {
            "incident_name": incident.get("scenario_name"),
            "status": "Completed",
            "duration": f"{incident.get('started_at', '')[:16]} to {incident.get('completed_at', '')[:16]}",
            "team_size": len(incident.get("team_members", [])),
            "actions_taken": len(incident.get("actions_taken", [])),
            "timeline_events": len(incident.get("timeline", [])),
            "score": incident.get("score"),
            "feedback": incident.get("feedback", []),
            "recommendations": [
                "Review detection capabilities",
                "Update incident response playbooks",
                "Conduct additional team training"
            ]
        }
    
    def get_mitre_mapping(self, technique_id: str = None) -> Dict:
        """Get MITRE ATT&CK technique information"""
        mitre_db = {
            "T1566.001": {"name": "Phishing: Spearphishing Attachment", "tactic": "Initial Access"},
            "T1204.002": {"name": "User Execution: Malicious File", "tactic": "Execution"},
            "T1486": {"name": "Data Encrypted for Impact", "tactic": "Impact"},
            "T1490": {"name": "Inhibit System Recovery", "tactic": "Impact"},
            "T1078": {"name": "Valid Accounts", "tactic": "Persistence"},
            "T1530": {"name": "Data from Cloud Storage", "tactic": "Collection"},
            "T1498": {"name": "Network Denial of Service", "tactic": "Impact"},
            "T1199": {"name": "Trusted Relationship", "tactic": "Initial Access"},
            "T1071": {"name": "Application Layer Protocol", "tactic": "Command and Control"}
        }
        
        if technique_id:
            return {"success": True, "technique": mitre_db.get(technique_id, {})}
        return {"success": True, "techniques": mitre_db}
    
    def get_certifications(self, user_id: str = None) -> Dict:
        """Get certification/progress data"""
        certs = self._load_certifications()
        if user_id:
            return {"success": True, "certification": certs.get(user_id, {})}
        return {"success": True, "all_certifications": certs}

soc_simulation = SOCSimulation()