# memory/long_term_memory.py

"""
Modulo: long_term_memory.py
Descrizione: Gestisce la memoria a lungo termine per Mercurius∞. Archivia e recupera ricordi strutturati
utilizzando un database locale SQLite.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

DB_PATH = "data/memory/long_term_memory.db"


class LongTermMemory:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    category TEXT,
                    content TEXT
                )
            ''')

    def store_memory(self, content: str, category: str = "general"):
        timestamp = datetime.now().isoformat()
        with self.conn:
            self.conn.execute('''
                INSERT INTO memories (timestamp, category, content)
                VALUES (?, ?, ?)
            ''', (timestamp, category, content))

    def retrieve_memories(self, category: Optional[str] = None, limit: int = 50) -> List[Tuple[str, str, str]]:
        cursor = self.conn.cursor()
        if category:
            cursor.execute('''
                SELECT timestamp, category, content FROM memories
                WHERE category = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT timestamp, category, content FROM memories
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        return cursor.fetchall()

    def search_memory(self, keyword: str, limit: int = 20) -> List[Tuple[str, str, str]]:
        cursor = self.conn.cursor()
        query = f'''
            SELECT timestamp, category, content FROM memories
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        cursor.execute(query, (f"%{keyword}%", limit))
        return cursor.fetchall()

    def close(self):
        self.conn.close()
