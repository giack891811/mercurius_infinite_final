# modules/experience/experience_memory.py

"""
Modulo: experience_memory.py
Descrizione: Memoria evolutiva esperienziale per il sistema Mercurius∞.
Registra segnali, trade e risultati; usa internamente il backend JSON di LongTermMemory.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from memory.long_term_memory import LongTermMemory


class ExperienceMemory:
    """
    Strato di astrazione sopra LongTermMemory (backend JSON) con API di alto livello per il trading.

    - Se config contiene la chiave "experience_file", userà quel file JSON (es. "memory/experience_log.json").
    - Mantiene, in aggiunta, una lista self.recent in memoria con le ultime N esperienze.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        - config: dizionario di configurazione. Se config["experience_file"] è presente, verrà usato come nome del file JSON.
        - In assenza di config, viene creato/riutilizzato “memory/experience_log.json”.
        """
        if config is None:
            config = {}

        # Decidiamo il percorso del file JSON: o quello fornito in config, oppure il default
        default_path = "memory/experience_log.json"
        self.storage_path: str = config.get("experience_file", default_path)

        # Creiamo la cartella se non esiste
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        # Inizializziamo LongTermMemory in modalità JSON, usando il file indicato
        self.store = LongTermMemory(
            backend="json",
            json_filename=self.storage_path
        )

        # Carichiamo la storia esistente dal file JSON, se esiste
        self.recent: List[Dict[str, Any]] = self._load_existing_history()

        # Massimo numero di esperienze da tenere in cache “recent”
        self._max_recent: int = config.get("max_recent", 50)

    def _load_existing_history(self) -> List[Dict[str, Any]]:
        """
        Legge il file JSON e restituisce la lista completa delle esperienze salvate.
        Popola self.recent con gli ultimi _max_recent elementi (o meno, se il file contiene di meno).
        """
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Se il file era vuoto o non ben formato, data potrebbe non essere lista
                if not isinstance(data, list):
                    return []
                # Manteniamo in recent solo gli ultimi max_recent elementi
                return data[-self._max_recent :]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def record_experience(
        self,
        signal: Any,
        trade: Any,
        result: Any,
        feedback: Any,
        tags: Optional[List[str]] = None
    ) -> None:
        """
        Registra una nuova esperienza di trading, composta da:
         - signal: informazioni sul segnale (es. "BUY EURUSD a 1.1000")
         - trade: dettagli del trade (es. numero di lotti, entry, exit)
         - result: risultato (es. profitto/perdita)
         - feedback: eventuali commenti o valutazioni
         - tags: lista opzionale di stringhe per categorizzare l’esperienza (di default ["trading"])
        """
        if tags is None:
            tags = ["trading"]

        # Costruiamo il dizionario dell’esperienza, aggiungendo timestamp UTC
        exp: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "signal": signal,
            "trade": trade,
            "result": result,
            "feedback": feedback,
            "tags": tags,
        }

        # Salviamo l’esperienza nel backend JSON di LongTermMemory
        self.store.save_experience(exp)

        # Aggiungiamo in cache
        self.recent.append(exp)
        # Se superiamo _max_recent, eliminiamo i più vecchi
        if len(self.recent) > self._max_recent:
            self.recent = self.recent[-self._max_recent :]

    def get_recent_experiences(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Restituisce le ultime 'limit' esperienze direttamente dalla cache self.recent.
        Se limit > len(recent), restituisce tutta la cache.
        """
        return self.recent[-limit:]

    def get_all_experiences(self) -> List[Dict[str, Any]]:
        """
        Legge tutte le esperienze dal file JSON (tramite LongTermMemory.get_all).
        Se si vuole lavorare con la lista completa, anche quelle non in cache.
        """
        return self.store.get_all()

    def reset(self) -> None:
        """
        Svuota completamente la memoria delle esperienze:
         - Cancella la cache self.recent
         - Sovrascrive il file JSON con lista vuota
        """
        self.recent.clear()
        # Sovrascriviamo il file JSON con lista vuota
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        except Exception as e:
            raise RuntimeError(f"Impossibile resettare il file '{self.storage_path}': {e}")

    def summarize(self) -> Dict[str, Any]:
        """
        Restituisce un dizionario riepilogativo della memoria:
         - 'total': numero totale di esperienze salvate
         - 'last_timestamp': timestamp dell’ultima esperienza (se esiste)
         - 'cached_recent': numero di esperienze in cache
        """
        all_exps = self.get_all_experiences()
        total = len(all_exps)
        last_ts = all_exps[-1]["timestamp"] if total > 0 else None
        return {
            "total": total,
            "last_timestamp": last_ts,
            "cached_recent": len(self.recent),
        }


# ===================== ESEMPIO DI UTILIZZO =====================
if __name__ == "__main__":
    # Esempio di configurazione: memorizza in 'memory/experience_log.json' e tiene 50 esperienze in cache
    config = {
        "experience_file": "memory/experience_log.json",
        "max_recent": 50
    }
    em = ExperienceMemory(config)

    # Registra un’esperienza di prova
    em.record_experience(
        signal={"symbol": "EURUSD", "type": "BUY", "price": 1.1000},
        trade={"lots": 0.1, "entry": 1.1000, "exit": 1.1020},
        result={"pnl": 20, "currency": "USD"},
        feedback="Buon segnale, gestione corretta dello stop."
    )

    # Ottieni le ultime 5 esperienze
    recenti = em.get_recent_experiences(limit=5)
    print("Ultime esperienze:", recenti)

    # Riassunto della memoria
    riassunto = em.summarize()
    print("Riepilogo:", riassunto)

    # Se vuoi resettare tutto, scommenta la riga seguente:
    # em.reset()
