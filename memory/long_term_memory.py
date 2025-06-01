"""
Modulo: long_term_memory.py
Descrizione: Gestisce la memoria a lungo termine per Mercurius∞.
Offre due possibili backend di archiviazione:
  - SQLite (database locale)
  - JSON/YAML (file locale)
L’utente può scegliere quale backend attivare passando il parametro 'backend' al costruttore.
"""

import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

# ----------------------------------------------------------------------
# CONFIGURAZIONE DEI PATH
# ----------------------------------------------------------------------

# Percorso del database SQLite
DB_PATH = Path("data/memory/long_term_memory.db")

# Cartella e file per il backend JSON
JSON_DIR  = Path("memory/long_term_data")
JSON_DIR.mkdir(parents=True, exist_ok=True)
JSON_DEFAULT_FILE = JSON_DIR / "experiences.json"

# ----------------------------------------------------------------------
# CLASSE: _SQLiteMemory
# ----------------------------------------------------------------------

class _SQLiteMemory:
    """
    Backend SQLite per la memoria a lungo termine.
    Crea una tabella 'memories' con i campi:
      - id (INTEGER PRIMARY KEY AUTOINCREMENT)
      - timestamp (TEXT)
      - category  (TEXT)
      - content   (TEXT)
    """

    def __init__(self, db_path: Union[str, Path] = DB_PATH):
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self._create_table()

    def _create_table(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    category  TEXT,
                    content   TEXT
                )
            """)

    def store_memory(self, content: str, category: str = "general") -> None:
        timestamp = datetime.utcnow().isoformat()
        with self.conn:
            self.conn.execute("""
                INSERT INTO memories (timestamp, category, content)
                VALUES (?, ?, ?)
            """, (timestamp, category, content))

    def retrieve_memories(self, category: Optional[str] = None, limit: int = 50) -> List[Tuple[str, str, str]]:
        cursor = self.conn.cursor()
        if category:
            cursor.execute("""
                SELECT timestamp, category, content FROM memories
                WHERE category = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (category, limit))
        else:
            cursor.execute("""
                SELECT timestamp, category, content FROM memories
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        return cursor.fetchall()

    def search_memory(self, keyword: str, limit: int = 20) -> List[Tuple[str, str, str]]:
        cursor = self.conn.cursor()
        query = """
            SELECT timestamp, category, content FROM memories
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        cursor.execute(query, (f"%{keyword}%", limit))
        return cursor.fetchall()

    def close(self) -> None:
        self.conn.close()

# ----------------------------------------------------------------------
# CLASSE: _JSONMemory
# ----------------------------------------------------------------------

class _JSONMemory:
    """
    Backend JSON per la memoria a lungo termine.
    Gestisce un file JSON contenente una lista di dizionari,
    ognuno con chiavi almeno: 'timestamp', 'content', eventualmente altre informazioni.
    """

    def __init__(self, filename: Union[str, Path] = JSON_DEFAULT_FILE):
        self.filepath = Path(filename)
        if not self.filepath.exists():
            self._write_json([])

    def save_experience(self, experience: Dict[str, Any]) -> None:
        experience["timestamp"] = datetime.utcnow().isoformat()
        data = self._read_json()
        data.append(experience)
        self._write_json(data)

    def get_all(self) -> List[Dict[str, Any]]:
        return self._read_json()

    def find_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        return [exp for exp in self._read_json() if tag in exp.get("tags", [])]

    def _read_json(self) -> List[Dict[str, Any]]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _write_json(self, data: List[Dict[str, Any]]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# ----------------------------------------------------------------------
# CLASSE PRINCIPALE: LongTermMemory
# ----------------------------------------------------------------------

class LongTermMemory:
    def __init__(
        self,
        backend: str = "sqlite",
        sqlite_path: Union[str, Path] = DB_PATH,
        json_filename: Union[str, Path] = JSON_DEFAULT_FILE
    ):
        backend = backend.lower()
        if backend not in ("sqlite", "json"):
            # Se backend è un file json, usa backend json
            if isinstance(backend, str) and backend.endswith(".json"):
                backend, json_filename = "json", Path(backend)
            else:
                raise ValueError("Il parametro 'backend' deve essere 'sqlite' o 'json'.")
        self.backend = backend

        if self.backend == "sqlite":
            self._db = _SQLiteMemory(db_path=sqlite_path)
        else:
            self._db = _JSONMemory(filename=json_filename)

    def store_memory(self, content: str, category: str = "general") -> None:
        if self.backend != "sqlite":
            raise RuntimeError("store_memory() disponibile solo con backend='sqlite'. Usa save_experience() per JSON.")
        self._db.store_memory(content, category)

    def retrieve_memories(self, category: Optional[str] = None, limit: int = 50) -> List[Tuple[str, str, str]]:
        if self.backend != "sqlite":
            raise RuntimeError("retrieve_memories() disponibile solo con backend='sqlite'.")
        return self._db.retrieve_memories(category=category, limit=limit)

    def search_memory(self, keyword: str, limit: int = 20) -> List[Tuple[str, str, str]]:
        if self.backend != "sqlite":
            raise RuntimeError("search_memory() disponibile solo con backend='sqlite'.")
        return self._db.search_memory(keyword, limit)

    def save_experience(self, experience: Dict[str, Any]) -> None:
        if self.backend != "json":
            raise RuntimeError("save_experience() disponibile solo con backend='json'. Usa store_memory() per SQLite.")
        self._db.save_experience(experience)

    def get_all(self) -> List[Dict[str, Any]]:
        if self.backend != "json":
            raise RuntimeError("get_all() disponibile solo con backend='json'.")
        return self._db.get_all()

    def find_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        if self.backend != "json":
            raise RuntimeError("find_by_tag() disponibile solo con backend='json'.")
        return self._db.find_by_tag(tag)

    def close(self) -> None:
        if self.backend == "sqlite":
            self._db.close()

# ======================================================================
# ESEMPIO DI UTILIZZO
# ======================================================================
if __name__ == "__main__":
    lm_sql = LongTermMemory(backend="sqlite")
    lm_sql.store_memory("Prima memoria di test", category="test")
    ricordi = lm_sql.retrieve_memories(limit=5)
    print("Ricordi da SQLite:", ricordi)
    lm_sql.close()

    lm_js = LongTermMemory(backend="json", json_filename=JSON_DIR / "test_experiences.json")
    lm_js.save_experience({"content": "Esperienza di prova", "category": "debug", "tags": ["test", "example"]})
    tutte = lm_js.get_all()
    print("Esperienze da JSON:", tutte)
