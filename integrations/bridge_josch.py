"""bridge_josch.py
===================
Interfaccia FastAPI per comunicare con il sistema "Josh" (alias JOSCH).

Il modulo espone un piccolo server FastAPI che consente l'esecuzione remota
di comandi su un sistema esterno e fornisce inoltre la funzione
``send_command_to_pc`` da utilizzare all'interno di Mercurius∞ per inviare
comandi al bridge.
"""

import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import uvicorn
import time

app = FastAPI(title="JOSCH Bridge")
start_time = time.time()


class CommandRequest(BaseModel):
    command: str
    mode: str = "cmd"  # cmd | powershell | python


@app.get("/ping")
def ping():
    return {"status": "online", "uptime": f"{int(time.time() - start_time)}s"}


@app.post("/cmd")
def run_command(req: CommandRequest):
    try:
        if req.mode == "cmd":
            result = subprocess.run(req.command, shell=True, capture_output=True, text=True)
        elif req.mode == "powershell":
            result = subprocess.run(["powershell", "-Command", req.command], capture_output=True, text=True)
        elif req.mode == "python":
            result = subprocess.run(["python", "-c", req.command], capture_output=True, text=True)
        else:
            raise HTTPException(status_code=400, detail="Invalid mode specified")

        return {
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def send_command_to_pc(command: str, mode: str = "cmd", base_url: str = "http://localhost:3020") -> dict:
    """Invia un comando al bridge JOSCH e restituisce la risposta JSON."""
    try:
        res = requests.post(
            f"{base_url}/cmd",
            json={"command": command, "mode": mode},
            timeout=5,
        )
        if res.status_code == 200:
            return res.json()
        return {"error": res.text, "status": res.status_code}
    except Exception as exc:
        return {"error": str(exc)}


def start_bridge(host="0.0.0.0", port=3020):
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_bridge()
