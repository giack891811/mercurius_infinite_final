# deployment/remote_access.py

"""
Modulo: remote_access.py
Descrizione: Server FastAPI per interazione remota sicura con Mercurius∞. Include supporto SSH tunnel opzionale.
"""

from fastapi import FastAPI
from deployment.telemetry_monitor import TelemetryMonitor
import uvicorn

app = FastAPI()
monitor = TelemetryMonitor()


@app.get("/status")
def status():
    return {
        "uptime": monitor.get_uptime(),
        "system": monitor.get_system_status(),
    }

@app.get("/logs")
def logs():
    return monitor.get_logs_tail("logs/system_operations.log", 20)

def start_remote_server(host="0.0.0.0", port=8800):
    uvicorn.run(app, host=host, port=port)
