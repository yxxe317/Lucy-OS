"""
Procedural memory - stores skills and procedures
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

class ProceduralMemory:
    """
    Stores skills, procedures, and how-to knowledge
    """
    
    def __init__(self, db_path="lucy_procedural.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Skills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                category TEXT,
                steps TEXT,
                prerequisites TEXT,
                examples TEXT,
                success_rate REAL,
                times_used INTEGER DEFAULT 0,
                created DATETIME,
                last_used DATETIME,
                tags TEXT
            )
        ''')
        
        # Procedures table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procedures (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                domain TEXT,
                input_schema TEXT,
                output_schema TEXT,
                code TEXT,
                api_endpoint TEXT,
                permissions TEXT,
                created DATETIME,
                version INTEGER
            )
        ''')
        
        # Usage logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_usage (
                id TEXT PRIMARY KEY,
                skill_id TEXT,
                timestamp DATETIME,
                success BOOLEAN,
                duration REAL,
                context TEXT,
                FOREIGN KEY(skill_id) REFERENCES skills(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_skill(self, name: str, description: str, steps: List[str],
                   category: str = "general", prerequisites: List[str] = None,
                   examples: List[str] = None, tags: List[str] = None) -> str:
        """
        Add a new skill
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        skill_id = hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:16]
        
        cursor.execute('''
            INSERT INTO skills
            (id, name, description, category, steps, prerequisites,
             examples, success_rate, times_used, created, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            skill_id, name, description, category,
            json.dumps(steps), json.dumps(prerequisites or []),
            json.dumps(examples or []), 1.0, 0, datetime.now(),
            json.dumps(tags or [])
        ))
        
        conn.commit()
        conn.close()
        
        return skill_id
    
    def get_skill(self, name: str) -> Optional[Dict]:
        """
        Retrieve a skill by name
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, category, steps, prerequisites,
                   examples, success_rate, times_used, last_used, tags
            FROM skills
            WHERE name = ?
        ''', (name,))
        
        row = cursor.fetchone()
        
        if row:
            # Update usage
            cursor.execute('''
                UPDATE skills
                SET times_used = ?, last_used = ?
                WHERE id = ?
            ''', (row[8] + 1, datetime.now(), row[0]))
            conn.commit()
            
            return {
                'id': row[0], 'name': row[1], 'description': row[2],
                'category': row[3], 'steps': json.loads(row[4]),
                'prerequisites': json.loads(row[5]) if row[5] else [],
                'examples': json.loads(row[6]) if row[6] else [],
                'success_rate': row[7], 'times_used': row[8] + 1,
                'last_used': row[9], 'tags': json.loads(row[10]) if row[10] else []
            }
        
        conn.close()
        return None
    
    def search_skills(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        Search for skills
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT id, name, description, category, success_rate, times_used
                FROM skills
                WHERE category = ? AND (name LIKE ? OR description LIKE ?)
                ORDER BY success_rate DESC, times_used DESC
                LIMIT 20
            ''', (category, f'%{query}%', f'%{query}%'))
        else:
            cursor.execute('''
                SELECT id, name, description, category, success_rate, times_used
                FROM skills
                WHERE name LIKE ? OR description LIKE ?
                ORDER BY success_rate DESC, times_used DESC
                LIMIT 20
            ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0], 'name': row[1], 'description': row[2],
            'category': row[3], 'success_rate': row[4], 'times_used': row[5]
        } for row in rows]
    
    def log_skill_usage(self, skill_id: str, success: bool, 
                         duration: float, context: Dict = None):
        """
        Log skill usage for learning
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        usage_id = hashlib.md5(f"{skill_id}{datetime.now()}".encode()).hexdigest()[:16]
        
        cursor.execute('''
            INSERT INTO skill_usage
            (id, skill_id, timestamp, success, duration, context)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (usage_id, skill_id, datetime.now(), success, duration,
              json.dumps(context or {})))
        
        # Update success rate
        cursor.execute('''
            SELECT COUNT(*), SUM(CASE WHEN success THEN 1 ELSE 0 END)
            FROM skill_usage
            WHERE skill_id = ?
        ''', (skill_id,))
        
        count, successes = cursor.fetchone()
        if count > 0:
            success_rate = successes / count
            
            cursor.execute('''
                UPDATE skills
                SET success_rate = ?
                WHERE id = ?
            ''', (success_rate, skill_id))
        
        conn.commit()
        conn.close()
    
    def get_categories(self) -> List[str]:
        """Get all skill categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT category FROM skills ORDER BY category')
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]
    
    def count(self) -> int:
        """Get number of skills"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM skills')
        count = cursor.fetchone()[0]
        conn.close()
        return count