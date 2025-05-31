# agents/agent_comm.py

"""
Modulo: agent_comm.py
Descrizione: Gestione della comunicazione tra agenti all'interno della rete Mercurius∞.
Permette lo scambio di messaggi strutturati tra agenti identificati da ID.
"""

from typing import Dict, List
from datetime import datetime

# Simulazione struttura di memorizzazione dei messaggi
MESSAGES: Dict[str, List[Dict]] = {}


def send_message(sender_id: str, receiver_id: str, content: str) -> None:
    """
    Invia un messaggio da un agente a un altro.
    """
    message = {
        "timestamp": datetime.now().isoformat(),
        "from": sender_id,
        "to": receiver_id,
        "content": content
    }
    if receiver_id not in MESSAGES:
        MESSAGES[receiver_id] = []
    MESSAGES[receiver_id].append(message)


def get_messages(agent_id: str) -> List[Dict]:
    """
    Recupera tutti i messaggi ricevuti da un agente.
    """
    return MESSAGES.get(agent_id, [])
