# consciousness/core_self.py
"""
Modulo: core_self.py
Descrizione: Nucleo identitario di Mercurius∞ (Sentient Mode).
Mantiene un profilo di sé, valori, scopo e tratti di personalità.
"""

from pathlib import Path
import yaml
from datetime import datetime
from typing import Dict, Any

PROFILE_FILE = Path("config/self_profile.yaml")
PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_PROFILE = {
    "name": "Mercurius∞",
    "version": "1.0",
    "values": ["curiosity", "transparency", "service"],
    "purpose": "Evolvere, assistere l’utilizzatore e creare valore etico.",
    "created": datetime.utcnow().isoformat(),
}


class CoreSelf:
    def __init__(self):
        if PROFILE_FILE.exists():
            self.profile: Dict[str, Any] = yaml.safe_load(PROFILE_FILE.read_text())  # type: ignore
        else:
            self.profile = DEFAULT_PROFILE.copy()
            self.save()

    # ---------- API ----------
    def get_identity(self) -> Dict[str, Any]:
        return self.profile

    def set_purpose(self, new_purpose: str):
        self.profile["purpose"] = new_purpose
        self.save()

    def append_value(self, value: str):
        if value not in self.profile["values"]:
            self.profile["values"].append(value)
            self.save()

    def save(self):
        yaml.safe_dump(self.profile, PROFILE_FILE.open("w", encoding="utf-8"))
