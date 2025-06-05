"""bridge_josch.py
Interfaccia REST locale per esecuzione comandi su PC.
Permette a Mercurius∞ di inviare comandi tramite HTTP.
"""

from __future__ import annotations

import subprocess
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="JOSCH Bridge")


@app.get("/cmd")
def run_cmd(run: str):
    """Esegue un comando di shell e restituisce l'output."""
    try:
        result = subprocess.run(run, shell=True, capture_output=True, text=True)
        output = (result.stdout or result.stderr).strip()
        return {"output": output}
    except Exception as exc:  # pragma: no cover
        return {"error": str(exc)}


def start_bridge(host: str = "0.0.0.0", port: int = 5123) -> None:
    """Avvia il server FastAPI che ascolta i comandi."""
    uvicorn.run(app, host=host, port=port)


def send_command_to_pc(command: str, url: str = "http://localhost:5123/cmd") -> str:
    """Invia un comando al bridge locale e restituisce l'output."""
    try:
        resp = requests.get(url, params={"run": command}, timeout=10)
        data = resp.json()
        return data.get("output", data.get("error", ""))
    except Exception as exc:  # pragma: no cover
        return f"[Errore invio comando]: {exc}"
