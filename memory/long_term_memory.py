# memory/long_term_memory.py

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
        # Assicuriamoci che la cartella esista
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Connessione al database
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
        """
        Inserisce un nuovo ricordo nella tabella SQLite.
        - content: testo del ricordo
        - category: stringa che identifica la categoria (es. "strategia", "lezione", "general"...)
        """
        timestamp = datetime.utcnow().isoformat()
        with self.conn:
            self.conn.execute("""
                INSERT INTO memories (timestamp, category, content)
                VALUES (?, ?, ?)
            """, (timestamp, category, content))

    def retrieve_memories(self, category: Optional[str] = None, limit: int = 50) -> List[Tuple[str, str, str]]:
        """
        Recupera fino a 'limit' ricordi ordinati per timestamp discendente.
        Se viene passata una categoria, restituisce solo i ricordi di quella categoria.
        Ritorna una lista di tuple (timestamp, category, content).
        """
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
        """
        Cerca all’interno del content di ogni ricordo la parola 'keyword'.
        Ritorna fino a 'limit' risultati ordinati per timestamp discendente.
        """
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
        """Chiude la connessione al database."""
        self.conn.close()


# ----------------------------------------------------------------------
# CLASSE: _JSONMemory
# ----------------------------------------------------------------------

class _JSONMemory:
    """
    Backend JSON per la memoria a lungo termine.
    Gestisce un file JSON (ad es. 'experiences.json') contenente una lista di dizionari,
    ognuno con chiavi almeno: 'timestamp', 'content', eventualmente altre informazioni.
    """

    def __init__(self, filename: Union[str, Path] = JSON_DEFAULT_FILE):
        self.filepath = Path(filename)
        # Se non esiste, creiamo il file con una lista vuota
        if not self.filepath.exists():
            self._write_json([])

    def save_experience(self, experience: Dict[str, Any]) -> None:
        """
        Salva (appende) una nuova esperienza nel file JSON.
        'experience' è un dizionario in cui verrà aggiunto automaticamente anche
        il campo 'timestamp' (UTC).
        Esempio di experience: {"content": "...", "category": "strategia", "tags": ["ml", "finanza"]}
        """
        experience["timestamp"] = datetime.utcnow().isoformat()
        data = self._read_json()
        data.append(experience)
        self._write_json(data)

    def get_all(self) -> List[Dict[str, Any]]:
        """Restituisce la lista completa di tutte le esperienze salvate (ordine di inserimento)."""
        return self._read_json()

    def find_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Restituisce tutte le esperienze in cui il campo 'tags' (lista) contiene 'tag'.
        Se in un dizionario non è presente 'tags', viene ignorato.
        """
        return [exp for exp in self._read_json() if tag in exp.get("tags", [])]

    def _read_json(self) -> List[Dict[str, Any]]:
        """Legge e restituisce il contenuto del file JSON come lista di dizionari."""
        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # In caso di file vuoto o danneggiato, ripristiniamo lista vuota
                return []

    def _write_json(self, data: List[Dict[str, Any]]) -> None:
        """
        Sovrascrive il file JSON con la lista 'data'.
        I dati vengono scritti con indentazione per leggibilità.
        """
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------------
# CLASSE PRINCIPALE: LongTermMemory
# ----------------------------------------------------------------------

class LongTermMemory:
    """
    Wrapper principale che espone un’unica interfaccia per la memoria a lungo termine.
    Parametri di inizializzazione:
      - backend: str, "sqlite" oppure "json"
      - sqlite_path: percorso opzionale del file database (se backend="sqlite")
      - json_filename: percorso opzionale del file JSON (se backend="json")

    Esempi:
      mem_sql = LongTermMemory(backend="sqlite")
      mem_sql.store_memory("Esempio di ricordo", category="generale")
      mem_sql.retrieve_memories(limit=10)

      mem_js = LongTermMemory(backend="json", json_filename="my_experiences.json")
      mem_js.save_experience({"content": "...", "category": "strategia", "tags": ["ai"]})
      tutte = mem_js.get_all()
      filtrate = mem_js.find_by_tag("ai")
    """

    def __init__(
        self,
        backend: str = "sqlite",
        sqlite_path: Union[str, Path] = DB_PATH,
        json_filename: Union[str, Path] = JSON_DEFAULT_FILE
    ):
        backend = backend.lower()
        if backend not in ("sqlite", "json"):
            raise ValueError("Il parametro 'backend' deve essere 'sqlite' o 'json'.")
        self.backend = backend

        if self.backend == "sqlite":
            # Inizializziamo il backend SQLite
            self._db = _SQLiteMemory(db_path=sqlite_path)
        else:
            # Inizializziamo il backend JSON
            self._db = _JSONMemory(filename=json_filename)

    # --- METODI COMUNI: stessa interfaccia, delegano al rispettivo backend ---

    def store_memory(self, content: str, category: str = "general") -> None:
        """
        Solo per backend SQLite: inserisce un ricordo.
        Per backend JSON va chiamato save_experience().
        """
        if self.backend != "sqlite":
            raise RuntimeError("store_memory() è disponibile solo con backend='sqlite'. "
                               "Usa save_experience() per il backend JSON.")
        self._db.store_memory(content, category)

    def retrieve_memories(
        self,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Tuple[str, str, str]]:
        """
        Solo per backend SQLite: recupera i ricordi.
        Ritorna lista di (timestamp, category, content).
        """
        if self.backend != "sqlite":
            raise RuntimeError("retrieve_memories() è disponibile solo con backend='sqlite'.")
        return self._db.retrieve_memories(category=category, limit=limit)

    def search_memory(
        self,
        keyword: str,
        limit: int = 20
    ) -> List[Tuple[str, str, str]]:
        """
        Solo per backend SQLite: cerca per parola chiave.
        """
        if self.backend != "sqlite":
            raise RuntimeError("search_memory() è disponibile solo con backend='sqlite'.")
        return self._db.search_memory(keyword, limit)

    def save_experience(self, experience: Dict[str, Any]) -> None:
        """
        Solo per backend JSON: salva (appende) un’esperienza nel file JSON.
        """
        if self.backend != "json":
            raise RuntimeError("save_experience() è disponibile solo con backend='json'. "
                               "Usa store_memory() per il backend SQLite.")
        self._db.save_experience(experience)

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Solo per backend JSON: ottiene tutte le esperienze salvate.
        """
        if self.backend != "json":
            raise RuntimeError("get_all() è disponibile solo con backend='json'.")
        return self._db.get_all()

    def find_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Solo per backend JSON: restituisce le esperienze che contengono il tag specificato.
        """
        if self.backend != "json":
            raise RuntimeError("find_by_tag() è disponibile solo con backend='json'.")
        return self._db.find_by_tag(tag)

    def close(self) -> None:
        """
        Chiude la connessione al database SQLite se si sta usando quel backend.
        Non fa nulla se backend='json'.
        """
        if self.backend == "sqlite":
            self._db.close()

# ======================================================================
# ESEMPIO DI UTILIZZO (puoi commentare o rimuovere questa sezione)
# ======================================================================
if __name__ == "__main__":
    # Esempio con SQLite
    lm_sql = LongTermMemory(backend="sqlite")
    lm_sql.store_memory("Prima memoria di test", category="test")
    ricordi = lm_sql.retrieve_memories(limit=5)
    print("Ricordi da SQLite:", ricordi)
    lm_sql.close()

    # Esempio con JSON
    lm_js = LongTermMemory(backend="json", json_filename=JSON_DIR / "test_experiences.json")
    lm_js.save_experience({"content": "Esperienza di prova", "category": "debug", "tags": ["test", "example"]})
    tutte = lm_js.get_all()
    print("Esperienze da JSON:", tutte)
