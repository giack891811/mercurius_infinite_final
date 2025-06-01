# integrations/agenda/agenda_manager.py
"""
Modulo: agenda_manager.py
Descrizione: Gestione eventi calendario (Google Calendar oppure ICS locale).
• crea_evento
• lista_eventi
• elimina_evento
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
import json

ICS_FILE = Path("integrations/agenda/local_calendar.json")  # fallback JSON

class AgendaManager:
    def __init__(self):
        self._load_local()

    # ---------- API Calendario ----------
    def crea_evento(self, titolo: str, start: datetime, end: datetime | None = None):
        event = {
            "id": len(self._events) + 1,
            "title": titolo,
            "start": start.isoformat(),
            "end": (end or start + timedelta(hours=1)).isoformat(),
        }
        self._events.append(event)
        self._save_local()
        return event

    def lista_eventi(self, date: datetime | None = None):
        if date:
            return [e for e in self._events if e["start"].startswith(date.date().isoformat())]
        return self._events

    def elimina_evento(self, event_id: int):
        self._events = [e for e in self._events if e["id"] != event_id]
        self._save_local()

    # ---------- interno ----------
    def _load_local(self):
        if ICS_FILE.exists():
            self._events = json.loads(ICS_FILE.read_text(encoding="utf-8"))
        else:
            self._events = []

    def _save_local(self):
        ICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        ICS_FILE.write_text(json.dumps(self._events, indent=2), encoding="utf-8")
