# monitoring/health_check.py

"""
Modulo: health_check.py
Descrizione: Endpoint di salute (liveness/readiness) per Mercurius∞ via FastAPI.
Espone:
  • GET /health → {"status": "ok", "uptime_sec": N}
  • GET /ready  → {"ready": true|false}

L'endpoint /health restituisce sempre "ok" finché il processo è in esecuzione,
mentre /ready diventa True solo se la variabile d'ambiente MERCURIUS_READY è settata a "true",
ad esempio quando l'orchestrator ha completato l'avvio completo di GENESIS_MODE.
"""

import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Mercurius∞ HealthCheck")
START_TIME = datetime.utcnow()


@app.get("/health")
def health():
    """
    Liveness probe:
    Restituisce sempre {"status": "ok", "uptime_sec": N}, dove N è il numero
    di secondi trascorsi dall'avvio di questo servizio.
    """
    uptime = (datetime.utcnow() - START_TIME).seconds
    return {"status": "ok", "uptime_sec": uptime}


@app.get("/ready")
def ready():
    """
    Readiness probe:
    Verifica se la variabile d'ambiente MERCURIUS_READY è impostata a "true".
    Restituisce {"ready": true} solo in quel caso, altrimenti {"ready": false}.
    Questo consente di segnalare che l'orchestrator (o il modulo GENESIS) è completamente avviato.
    """
    ready_flag = os.getenv("MERCURIUS_READY", "false").lower() == "true"
    return {"ready": ready_flag}


if __name__ == "__main__":
    # Esegue il server FastAPI su tutte le interfacce di rete (0.0.0.0) alla porta 8080
    uvicorn.run(app, host="0.0.0.0", port=8080)
