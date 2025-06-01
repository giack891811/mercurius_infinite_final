# modules/n8n_connector.py

"""
Modulo: n8n_connector.py
Descrizione: Invio e ricezione webhook da n8n per orchestrare flussi AI → PC locale.
"""

import requests

class N8NConnector:
    def __init__(self, webhook_url="http://localhost:5678/webhook/test"):
        self.webhook_url = webhook_url

    def trigger_flow(self, payload: dict) -> str:
        try:
            res = requests.post(self.webhook_url, json=payload)
            return f"📡 Webhook n8n attivato: {res.status_code}"
        except Exception as e:
            return f"❌ Errore n8n: {str(e)}"
