import aiosqlite
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger("LucyMemory")

class MemorySystem:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "lucy_memory.db"
        self.initialized = False

    async def init_db(self):
        if self.initialized:
            return
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    query TEXT,
                    response TEXT
                )
            """)
            await db.commit()
        
        self.initialized = True
        logger.info("💾 Memory System Initialized.")

    async def save_interaction(self, query: str, response: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO interactions (timestamp, query, response) VALUES (?, ?, ?)",
                (datetime.now().isoformat(), query, response)
            )
            await db.commit()
        logger.info(f"💾 Saved interaction: {query[:20]}...")

    async def get_history(self, limit: int = 10):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM interactions ORDER BY id DESC LIMIT ?", (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

memory = MemorySystem()