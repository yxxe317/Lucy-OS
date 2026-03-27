"""
Orchestrator Layer - Routines 121-140+
Supervised Autonomy with MCP Protocol and Hardware-Software Synergy
"""

import os
import json
import asyncio
import time
import re
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import threading
import psutil
import subprocess
import httpx
import numpy as np

# Try to import optional dependencies
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

# Configuration
BASE_DIR = Path(__file__).parent.parent
ORCHESTRATOR_CONFIG = os.path.join(BASE_DIR, 'config', 'orchestrator_config.json')
MCP_SERVERS_CONFIG = os.path.join(BASE_DIR, 'config', 'mcp_servers.json')
REASONING_LOG_PATH = os.path.join(BASE_DIR, 'logs', 'reasoning_tree.jsonl')
DATA_SHREDDER_PATH = os.path.join(BASE_DIR, 'data', 'shredded_credentials.json')
THERMAL_MAP_PATH = os.path.join(BASE_DIR, 'data', 'thermal_map.json')

# Ensure directories exist
os.makedirs(os.path.dirname(REASONING_LOG_PATH), exist_ok=True)
os.makedirs(os.path.dirname(DATA_SHREDDER_PATH), exist_ok=True)
os.makedirs(os.path.dirname(THERMAL_MAP_PATH), exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [ORCHESTRATOR] %(message)s'
)
logger = logging.getLogger("Orchestrator")

# ============================================================================
# DATA CLASSES
# ============================================================================

class RoutineStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    APPROVAL_REQUIRED = "approval_required"

@dataclass
class ReasoningNode:
    node_id: str
    action: str
    rationale: str
    confidence: float
    timestamp: str
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    status: str = "pending"

@dataclass
class VRAMModel:
    name: str
    vram_usage: int
    confidence_threshold: float
    capability_score: float
    active: bool = False

@dataclass
class MCPServer:
    name: str
    command: str
    args: List[str]
    tools: List[str]
    status: str = "disconnected"

@dataclass
class ThermalProfile:
    prompt_complexity: float
    fan_speed: int
    power_limit: int
    temperature_target: float

# ============================================================================
# MCP SWARM (Routine 121)
# ============================================================================

class MCPSwarm:
    """MCP Swarm - Connect to external MCP servers to execute tools"""
    
    def __init__(self):
        self.servers: Dict[str, Any] = {}
        self.available_tools: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        
    async def connect_server(self, server_config: MCPServer) -> bool:
        """Connect to an MCP server"""
        try:
            if not MCP_AVAILABLE:
                logger.warning("MCP SDK not available")
                return False
                
            server_params = StdioServerParameters(
                command=server_config.command,
                args=server_config.args,
                env=os.environ.copy()
            )
            
            stdio_transport = await stdio_client(server_params)
            session = ClientSession(stdio_transport)
            
            await session.initialize()
            
            with self._lock:
                self.servers[server_config.name] = session
            
            logger.info(f"✅ MCP Server connected: {server_config.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ MCP Server connection failed ({server_config.name}): {e}")
            return False
    
    async def list_tools(self) -> List[Dict]:
        """List all available tools from connected servers"""
        tools = []
        
        with self._lock:
            for name, session in self.servers.items():
                try:
                    tools_response = await session.list_tools()
                    for tool in tools_response.tools:
                        tools.append({
                            "server": name,
                            "name": tool.name,
                            "description": tool.description
                        })
                except Exception as e:
                    logger.error(f"Failed to list tools from {name}: {e}")
        
        return tools
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Any:
        """Call a tool from an MCP server"""
        with self._lock:
            if server_name not in self.servers:
                raise ValueError(f"MCP server not connected: {server_name}")
            
            session = self.servers[server_name]
            
        try:
            call_result = await session.call_tool(tool_name, arguments)
            return call_result
        except Exception as e:
            logger.error(f"Tool call failed ({server_name}/{tool_name}): {e}")
            raise
    
    async def discover_servers(self, config_path: str = MCP_SERVERS_CONFIG) -> List[MCPServer]:
        """Discover available MCP servers from config"""
        servers = []
        
        if not os.path.exists(config_path):
            logger.warning(f"MCP config not found: {config_path}")
            return servers
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        for server_name, server_config in config.items():
            server = MCPServer(
                name=server_name,
                command=server_config.get('command', ''),
                args=server_config.get('args', []),
                tools=server_config.get('tools', [])
            )
            servers.append(server)
        
        return servers

# Global MCP Swarm instance
mcp_swarm = MCPSwarm()

# ============================================================================
# AUTONOMOUS LEAD-GEN (Routine 122)
# ============================================================================

class AutonomousLeadGen:
    """Autonomous Lead-Gen - Scrape B2B directories for prospects"""
    
    def __init__(self):
        self.lead_database = []
        self._lock = threading.Lock()
        
    def scrape_linkedin(self, keywords: List[str], location: str = None) -> List[Dict]:
        """Scrape LinkedIn for prospects (simulated)"""
        leads = []
        sample_leads = [
            {
                "name": "John Smith",
                "company": "TechCorp Inc.",
                "position": "CTO",
                "industry": "AI/ML",
                "location": location or "San Francisco, CA",
                "email": "john.smith@techcorp.com",
                "linkedin": "linkedin.com/in/johnsmith",
                "score": 0.85
            },
            {
                "name": "Sarah Johnson",
                "company": "DataFlow Systems",
                "position": "VP of Engineering",
                "industry": "Data Analytics",
                "location": location or "New York, NY",
                "email": "sarah.j@dataflow.com",
                "linkedin": "linkedin.com/in/sarahjohnson",
                "score": 0.92
            }
        ]
        
        for lead in sample_leads:
            if any(keyword in lead.get('industry', '').lower() for keyword in keywords):
                leads.append(lead)
        
        return leads
    
    def scrape_b2b_directory(self, url: str) -> List[Dict]:
        """Scrape B2B directory for prospects"""
        leads = []
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    leads = self._parse_response(response.text)
        except Exception as e:
            logger.error(f"Scrape failed: {e}")
        return leads
    
    def _parse_response(self, html: str) -> List[Dict]:
        """Parse scraped HTML for lead data"""
        leads = []
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, html)
        company_pattern = r'(?:company|organization|business)\s*[:=]\s*([^\n,]+)'
        companies = re.findall(company_pattern, html, re.IGNORECASE)
        
        for email in emails:
            lead = {
                "email": email,
                "company": companies[0] if companies else "Unknown",
                "source": "B2B Directory",
                "score": 0.7
            }
            leads.append(lead)
        return leads
    
    def save_leads(self, leads: List[Dict], filename: str = None):
        """Save leads to database"""
        if not filename:
            filename = f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with self._lock:
            self.lead_database.extend(leads)
        
        filepath = os.path.join(BASE_DIR, 'data', filename)
        with open(filepath, 'w') as f:
            json.dump(self.lead_database, f, indent=2)
        
        logger.info(f"✅ Saved {len(leads)} leads to {filename}")

# Global Lead Gen instance
lead_gen = AutonomousLeadGen()

# ============================================================================
# NPU OFFLOADER (Routine 123)
# ============================================================================

class NPUOffloader:
    """NPU Offloader - Move non-critical NLP tasks to NPU"""
    
    def __init__(self):
        self.npu_available = False
        self.offloaded_tasks = []
        
    def check_npu_availability(self) -> bool:
        """Check if NPU is available"""
        try:
            result = subprocess.run(
                ['npu-smi', 'info'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.npu_available = True
                logger.info("✅ NPU detected and available")
                return True
            else:
                logger.warning("⚠️ NPU not detected")
                return False
        except Exception as e:
            logger.error(f"NPU check failed: {e}")
            return False
    
    def should_offload(self, task_type: str, vram_usage: int) -> bool:
        """Determine if task should be offloaded to NPU"""
        critical_tasks = ['inference', 'training', 'fine_tuning']
        if task_type in critical_tasks:
            return False
        return vram_usage > 60
    
    def offload_task(self, task: Dict) -> bool:
        """Offload a task to NPU"""
        if not self.npu_available:
            return False
        try:
            self.offloaded_tasks.append(task)
            logger.info(f"✅ Task offloaded to NPU: {task.get('name', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Offload failed: {e}")
            return False

# Global NPU Offloader instance
npu_offloader = NPUOffloader()

# ============================================================================
# GHOST REVIEWER (Routine 124)
# ============================================================================

class GhostReviewer:
    """Ghost Reviewer - Inject Senior Dev feedback via custom LSP"""
    
    def __init__(self):
        self.review_queue = []
        self._lock = threading.Lock()
        
    def analyze_code(self, code: str, file_path: str = None) -> List[Dict]:
        """Analyze code and generate review feedback"""
        reviews = []
        issues = self._check_code_quality(code)
        
        for issue in issues:
            review = {
                "file": file_path or "unknown",
                "line": issue.get('line', 0),
                "severity": issue.get('severity', 'info'),
                "message": issue.get('message', ''),
                "suggestion": issue.get('suggestion', '')
            }
            reviews.append(review)
        return reviews
    
    def _check_code_quality(self, code: str) -> List[Dict]:
        """Check code quality and generate feedback"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if re.search(r'(TODO|FIXME|XXX|HACK)', line, re.IGNORECASE):
                issues.append({
                    "line": i,
                    "severity": "warning",
                    "message": f"Found {re.search(r'(TODO|FIXME|XXX|HACK)', line, re.IGNORECASE).group()}",
                    "suggestion": "Consider implementing this feature or fixing this issue"
                })
        
        function_depth = 0
        for i, line in enumerate(lines, 1):
            if re.search(r'\b(def|function|async def)\b', line):
                function_depth += 1
                if function_depth > 3:
                    issues.append({
                        "line": i,
                        "severity": "warning",
                        "message": "Nested function depth exceeds 3 levels",
                        "suggestion": "Consider refactoring into smaller functions"
                    })
                function_depth = 0
        
        for i, line in enumerate(lines, 1):
            if re.search(r'\bdef\s+\w+\s*\(', line) and not re.search(r':\s*\w+', line):
                issues.append({
                    "line": i,
                    "severity": "info",
                    "message": "Missing type hints",
                    "suggestion": "Add type hints for better code documentation"
                })
        
        return issues
    
    def inject_review(self, review: Dict) -> bool:
        """Inject review into VS Code via LSP"""
        try:
            self.review_queue.append(review)
            logger.info(f"✅ Review injected: {review.get('message', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Review injection failed: {e}")
            return False
    
    def get_pending_reviews(self) -> List[Dict]:
        """Get pending reviews"""
        with self._lock:
            return self.review_queue.copy()
    
    def clear_reviews(self):
        """Clear all reviews"""
        with self._lock:
            self.review_queue.clear()
            logger.info("✅ All reviews cleared")

# Global Ghost Reviewer instance
ghost_reviewer = GhostReviewer()

# ============================================================================
# AGENTIC SEO (Routine 125)
# ============================================================================

class AgenticSEO:
    """Agentic SEO - Audit LLM-readability of web projects"""
    
    def __init__(self):
        self.audit_results = []
        
    def audit_readability(self, content: str) -> Dict:
        """Audit content for LLM-readability"""
        metrics = {
            "flesch_reading_ease": self._calculate_flesch(content),
            "flesch_kincaid_grade": self._calculate_flesch_kincaid(content),
            "gunning_fog": self._calculate_gunning_fog(content),
            "smog_index": self._calculate_smoG(content),
            "avg_sentence_length": self._calculate_avg_sentence_length(content),
            "avg_word_length": self._calculate_avg_word_length(content),
            "passive_voice_ratio": self._calculate_passive_voice_ratio(content),
            "readability_score": self._calculate_readability_score(content)
        }
        return metrics
    
    def _calculate_flesch(self, text: str) -> float:
        """Calculate Flesch Reading Ease score"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        syllables = sum(self._count_syllables(word) for word in words)
        
        if len(words) > 0 and len(sentences) > 0:
            score = 206.835 - (1.015 * (len(words) / len(sentences))) - (84.6 * (syllables / len(words)))
            return max(0, min(100, score))
        return 0
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        word = re.sub(r'[aeiouy]', ' ', word, flags=re.IGNORECASE)
        return len([w for w in word.split() if w])
    
    def _calculate_flesch_kincaid(self, text: str) -> float:
        """Calculate Flesch-Kincaid Grade Level"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        syllables = sum(self._count_syllables(word) for word in words)
        
        if len(words) > 0 and len(sentences) > 0:
            grade = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59
            return max(0, grade)
        return 0
    
    def _calculate_gunning_fog(self, text: str) -> float:
        """Calculate Gunning Fog Index"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        complex_words = len([w for w in words if self._count_syllables(w) >= 3])
        
        if len(words) > 0 and len(sentences) > 0:
            fog = 0.4 * ((len(words) / len(sentences)) + (100 * complex_words / len(words)))
            return fog
        return 0
    
    def _calculate_smoG(self, text: str) -> float:
        """Calculate SMOG Index"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        polysyllabic = len([w for w in words if self._count_syllables(w) >= 3])
        
        if len(sentences) > 0:
            smog = 1.043 * (polysyllabic ** 0.5 * len(sentences) ** 0.5) + 3.1291
            return smog
        return 0
    
    def _calculate_avg_sentence_length(self, text: str) -> float:
        """Calculate average sentence length"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        if len(sentences) > 0:
            return len(words) / len(sentences)
        return 0
    
    def _calculate_avg_word_length(self, text: str) -> float:
        """Calculate average word length"""
        words = [w for w in text.split() if w]
        if words:
            return sum(len(w) for w in words) / len(words)
        return 0
    
    def _calculate_passive_voice_ratio(self, text: str) -> float:
        """Calculate passive voice ratio"""
        passive_patterns = [r'\bwas\s+[\w]+', r'\bwere\s+[\w]+', r'\bbeen\s+[\w]+']
        matches = sum(1 for pattern in passive_patterns if re.search(pattern, text, re.IGNORECASE))
        total_verbs = len(re.findall(r'\b\w+ed\b', text, re.IGNORECASE))
        
        if total_verbs > 0:
            return matches / total_verbs
        return 0
    
    def _calculate_readability_score(self, text: str) -> str:
        """Calculate overall readability score"""
        metrics = self.audit_readability(text)
        score = metrics['flesch_reading_ease']
        
        if score >= 80:
            return "Excellent - Easy to read"
        elif score >= 60:
            return "Good - Standard readability"
        elif score >= 50:
            return "Fair - Somewhat difficult"
        elif score >= 30:
            return "Difficult - Challenging"
        else:
            return "Very Difficult - Expert level only"
    
    def audit_project(self, project_path: str) -> Dict:
        """Audit entire project for SEO/readability"""
        results = {
            "project": project_path,
            "timestamp": datetime.now().isoformat(),
            "files_audited": 0,
            "issues": [],
            "recommendations": []
        }
        
        for file_path in Path(project_path).rglob('*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metrics = self.audit_readability(content)
                results['files_audited'] += 1
                
                if metrics['flesch_reading_ease'] < 50:
                    results['issues'].append({
                        "file": str(file_path),
                        "issue": "Low readability score",
                        "metrics": metrics
                    })
            except Exception as e:
                logger.error(f"Failed to audit {file_path}: {e}")
        
        return results

# Global Agentic SEO instance
agentic_seo = AgenticSEO()

# ============================================================================
# DATA SHREDDER (Routine 127)
# ============================================================================

class DataShredder:
    """Data Shredder - Identify and encrypt plaintext credentials"""
    
    def __init__(self):
        self.shredded_credentials = []
        self._lock = threading.Lock()
        
    def scan_file(self, file_path: str) -> List[Dict]:
        """Scan file for plaintext credentials"""
        credentials = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            credential_patterns = [
                (r'(?i)(api[_-]?key|apikey|secret|password|token)\s*[=:]\s*["\']?([a-zA-Z0-9_\-]+)', 'credential'),
                (r'(?i)aws[_-]?access[_-]?key[_-]?id\s*[=:]\s*["\']?([A-Z0-9]+)', 'aws_key'),
                (r'(?i)stripe[_-]?secret[_-]?key\s*[=:]\s*["\']?([a-zA-Z0-9]+)', 'stripe_key'),
                (r'(?i)google[_-]?api[_-]?key\s*[=:]\s*["\']?([a-zA-Z0-9]+)', 'google_key'),
            ]
            
            for pattern, cred_type in credential_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    credentials.append({
                        "file": file_path,
                        "type": cred_type,
                        "line": content[:match.start()].count('\n') + 1,
                        "value": match.group(0),
                        "redacted": self._redact_value(match.group(0))
                    })
        except Exception as e:
            logger.error(f"Scan failed for {file_path}: {e}")
        
        return credentials
    
    def _redact_value(self, value: str) -> str:
        """Redact sensitive value"""
        if len(value) > 20:
            return value[:7] + '*' * (len(value) - 7)
        return '*' * len(value)
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[Dict]:
        """Scan directory for credentials"""
        all_credentials = []
        
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file():
                if 'shredded' in str(file_path):
                    continue
                credentials = self.scan_file(str(file_path))
                all_credentials.extend(credentials)
        
        return all_credentials
    
    def shred_credentials(self, credentials: List[Dict]) -> List[Dict]:
        """Shred (encrypt/redact) credentials"""
        shredded = []
        
        for cred in credentials:
            shredded_cred = cred.copy()
            shredded_cred['redacted'] = self._redact_value(cred['value'])
            shredded_cred['shredded_at'] = datetime.now().isoformat()
            shredded.append(shredded_cred)
        
        with self._lock:
            self.shredded_credentials.extend(shredded)
        
        self._save_shredded_credentials()
        logger.info(f"✅ Shredded {len(shredded)} credentials")
        return shredded
    
    def _save_shredded_credentials(self):
        """Save shredded credentials to file"""
        filepath = DATA_SHREDDER_PATH
        with open(filepath, 'w') as f:
            json.dump(self.shredded_credentials, f, indent=2)
    
    def get_shredded_credentials(self) -> List[Dict]:
        """Get list of shredded credentials"""
        with self._lock:
            return self.shredded_credentials.copy()
    
    def auto_scan(self, directory: str = None, interval_hours: float = 6):
        """Auto-scan directory every interval_hours"""
        if directory is None:
            directory = str(BASE_DIR)
        
        while True:
            try:
                credentials = self.scan_directory(directory)
                if credentials:
                    self.shred_credentials(credentials)
            except Exception as e:
                logger.error(f"Auto-scan failed: {e}")
            
            time.sleep(interval_hours * 3600)

# Global Data Shredder instance
data_shredder = DataShredder()

# ============================================================================
# THERMAL SHIELD (Routine 130)
# ============================================================================

class ThermalShield:
    """Thermal Shield - Map prompt complexity to Fan PWM curves"""
    
    def __init__(self):
        self.thermal_profile = self._load_thermal_profile()
        self._lock = threading.Lock()
        
    def _load_thermal_profile(self) -> Dict[str, ThermalProfile]:
        """Load thermal profile from file"""
        if os.path.exists(THERMAL_MAP_PATH):
            with open(THERMAL_MAP_PATH, 'r') as f:
                data = json.load(f)
            return {
                str(k): ThermalProfile(**v) 
                for k, v in data.get('profiles', {}).items()
            }
        return {}
    
    def _save_thermal_profile(self):
        """Save thermal profile to file"""
        profile = {
            "profiles": {k: asdict(v) for k, v in self.thermal_profile.items()},
            "last_updated": datetime.now().isoformat()
        }
        
        with open(THERMAL_MAP_PATH, 'w') as f:
            json.dump(profile, f, indent=2)
    
    def calculate_prompt_complexity(self, prompt: str) -> float:
        """Calculate prompt complexity score (0-1)"""
        score = 0.0
        score += min(len(prompt) / 10000, 0.3)
        tokens = len(prompt.split())
        score += min(tokens / 500, 0.3)
        special_chars = sum(1 for c in prompt if not c.isalnum() and not c.isspace())
        score += min(special_chars / 100, 0.2)
        
        depth = 0
        for c in prompt:
            if c in ['(', '[', '{']:
                depth += 1
            elif c in [')', ']', '}']:
                depth -= 1
        score += min(depth / 10, 0.2)
        
        return min(score, 1.0)
    
    def get_thermal_profile(self, complexity: float) -> ThermalProfile:
        """Get thermal profile for given complexity"""
        sorted_profiles = sorted(
            self.thermal_profile.items(),
            key=lambda x: x[1].prompt_complexity
        )
        
        for profile in sorted_profiles:
            if profile[1].prompt_complexity >= complexity:
                return profile[1]
        
        return sorted_profiles[-1][1] if sorted_profiles else ThermalProfile(
            prompt_complexity=1.0,
            fan_speed=2000,
            power_limit=125,
            temperature_target=75
        )
    
    def adjust_fan_curve(self, target_speed: int):
        """Adjust fan curve to target speed"""
        try:
            result = subprocess.run(
                ['msiafterburn', '/set', str(target_speed)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Fan curve adjusted to {target_speed} RPM")
                return True
            else:
                logger.warning(f"⚠️ Failed to adjust fan curve")
                return False
        except Exception as e:
            logger.error(f"Fan adjustment failed: {e}")
            return False
    
    def monitor_temperature(self) -> Dict:
        """Monitor current temperature"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                temp = float(result.stdout.strip())
                return {"temperature": temp, "unit": "°C"}
        except Exception as e:
            logger.error(f"Temperature monitoring failed: {e}")
        
        return {"temperature": None, "unit": "°C"}
    
    def get_optimal_fan_speed(self, prompt: str) -> int:
        """Get optimal fan speed for given prompt"""
        complexity = self.calculate_prompt_complexity(prompt)
        profile = self.get_thermal_profile(complexity)
        return profile.fan_speed

# Global Thermal Shield instance
thermal_shield = ThermalShield()

# ============================================================================
# REASONING TREE (Routine 131)
# ============================================================================

class ReasoningTree:
    """Reasoning Tree - Generate 'Why' log for every autonomous action"""
    
    def __init__(self):
        self.nodes: Dict[str, ReasoningNode] = {}
        self.root_node_id = None
        self._lock = threading.Lock()
        
    def log_action(self, action: str, rationale: str, confidence: float = 0.5) -> str:
        """Log an action with reasoning"""
        node_id = hashlib.md5(f"{action}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        node = ReasoningNode(
            node_id=node_id,
            action=action,
            rationale=rationale,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
        with self._lock:
            self.nodes[node_id] = node
            
            if self.root_node_id is None:
                self.root_node_id = node_id
            else:
                parent = self._find_parent(node_id)
                if parent:
                    self.nodes[parent].children.append(node_id)
        
        self._log_to_file(node)
        logger.info(f"🌳 Reasoning: {action} - {rationale[:50]}...")
        return node_id
    
    def _find_parent(self, node_id: str) -> Optional[str]:
        """Find parent node for new action"""
        if not self.nodes:
            return None
        
        recent_nodes = list(self.nodes.values())[-5:]
        for node in recent_nodes:
            if node.status == "pending":
                return node.node_id
        
        return None
    
    def _log_to_file(self, node: ReasoningNode):
        """Log node to file"""
        filepath = REASONING_LOG_PATH
        with open(filepath, 'a') as f:
            f.write(json.dumps(asdict(node)) + '\n')
    
    def get_tree(self) -> Dict:
        """Get full reasoning tree"""
        with self._lock:
            return {
                "root": self.root_node_id,
                "nodes": {k: asdict(v) for k, v in self.nodes.items()}
            }
    
    def clear_tree(self):
        """Clear reasoning tree"""
        with self._lock:
            self.nodes.clear()
            self.root_node_id = None
        logger.info("✅ Reasoning tree cleared")

# Global Reasoning Tree instance
reasoning_tree = ReasoningTree()

# ============================================================================
# MODEL AUCTION (Routine 132)
# ============================================================================

class ModelAuction:
    """Model Auction - Route tasks to lowest VRAM model meeting confidence threshold"""
    
    def __init__(self):
        self.models: Dict[str, VRAMModel] = {}
        self._lock = threading.Lock()
        
    def register_model(self, model: VRAMModel):
        """Register a model for auction"""
        with self._lock:
            self.models[model.name] = model
            logger.info(f"✅ Model registered: {model.name} ({model.vram_usage} MB VRAM)")
    
    def find_best_model(self, task_type: str, required_confidence: float) -> Optional[VRAMModel]:
        """Find the best model for the task"""
        eligible_models = [
            m for m in self.models.values()
            if m.confidence_threshold <= required_confidence and m.active
        ]
        
        if not eligible_models:
            return None
        
        # Sort by VRAM usage (lowest first)
        eligible_models.sort(key=lambda m: m.vram_usage)
        return eligible_models[0]
    
    def auction_task(self, task: Dict) -> Optional[str]:
        """Run auction for task and return winning model name"""
        required_confidence = task.get('confidence_threshold', 0.5)
        best_model = self.find_best_model(task.get('type', 'default'), required_confidence)
        
        if best_model:
            logger.info(f"🏆 Model won auction: {best_model.name}")
            return best_model.name
        return None

# Global Model Auction instance
model_auction = ModelAuction()

# ============================================================================
# ORCHESTRATOR MAIN CLASS
# ============================================================================

class Orchestrator:
    """Main Orchestrator - Coordinates all routines"""
    
    def __init__(self):
        self.active_routines: Dict[str, RoutineStatus] = {}
        self._lock = threading.Lock()
        
    def register_routine(self, routine_name: str, routine_instance):
        """Register a routine"""
        self.active_routines[routine_name] = RoutineStatus.IDLE
        logger.info(f"✅ Routine registered: {routine_name}")
    
    def start_routine(self, routine_name: str) -> bool:
        """Start a routine"""
        with self._lock:
            if routine_name not in self.active_routines:
                logger.error(f"Routine not found: {routine_name}")
                return False
            
            self.active_routines[routine_name] = RoutineStatus.RUNNING
            logger.info(f"🚀 Starting routine: {routine_name}")
            return True
    
    def stop_routine(self, routine_name: str) -> bool:
        """Stop a routine"""
        with self._lock:
            if routine_name not in self.active_routines:
                logger.error(f"Routine not found: {routine_name}")
                return False
            
            self.active_routines[routine_name] = RoutineStatus.PAUSED
            logger.info(f"⏸️ Routine paused: {routine_name}")
            return True
    
    def get_status(self) -> Dict[str, str]:
        """Get status of all routines"""
        with self._lock:
            return dict(self.active_routines)
    
    def run_all(self):
        """Run all registered routines"""
        for routine_name in self.active_routines:
            self.start_routine(routine_name)

# Global Orchestrator instance
orchestrator = Orchestrator()

# Register all routines
orchestrator.register_routine("mcp_swarm", mcp_swarm)
orchestrator.register_routine("lead_gen", lead_gen)
orchestrator.register_routine("npu_offloader", npu_offloader)
orchestrator.register_routine("ghost_reviewer", ghost_reviewer)
orchestrator.register_routine("agentic_seo", agentic_seo)
orchestrator.register_routine("data_shredder", data_shredder)
orchestrator.register_routine("thermal_shield", thermal_shield)
orchestrator.register_routine("reasoning_tree", reasoning_tree)
orchestrator.register_routine("model_auction", model_auction)

logger.info("🚀 Orchestrator initialized successfully")