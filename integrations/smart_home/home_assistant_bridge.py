# integrations/smart_home/home_assistant_bridge.py
"""
Modulo: home_assistant_bridge.py
Descrizione: Controlla dispositivi Home Assistant via REST API.
"""

import os
import requests

HASS_URL = os.getenv("HASS_URL", "http://localhost:8123")
HASS_TOKEN = os.getenv("HASS_TOKEN", "")

HEADERS = {"Authorization": f"Bearer {HASS_TOKEN}", "Content-Type": "application/json"}

class HomeAssistantBridge:
    def call_service(self, domain: str, service: str, data: dict):
        url = f"{HASS_URL}/api/services/{domain}/{service}"
        r = requests.post(url, json=data, headers=HEADERS, timeout=5)
        return r.ok

    # esempi pratici
    def turn_on_light(self, entity_id: str):
        return self.call_service("light", "turn_on", {"entity_id": entity_id})

    def set_temperature(self, entity_id: str, temp: float):
        return self.call_service("climate", "set_temperature",
                                 {"entity_id": entity_id, "temperature": temp})
