"""
Modulo: n8n_connector.py
Responsabilità: Interfaccia per workflow automation tramite n8n (API, webhook).
Autore: Mercurius∞ AI Engineer
"""

import requests

class N8NConnector:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or "http://localhost:5678/webhook/test"
    
    def is_available(self):
        # Prova di reachability
        try:
            response = requests.get(self.webhook_url, timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def run_task(self, payload: dict):
        """
        Invia un payload a un workflow n8n tramite webhook POST.
        """
        if not self.is_available():
            return "[❌ n8n non raggiungibile]"
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            return f"Risposta n8n: {response.status_code} - {response.text}"
        except Exception as e:
            return f"[❌ Errore n8n]: {e}"
