"""
bridge_josch.py
===============
Interfaccia FastAPI per comunicare con il sistema "Josh" (alias JOSCH).

Il modulo espone:
1) Bridge di comandi shell / python
2) Webhook TradingView
3) API file-system permanenti (Mercurius∞)
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path

import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 📦 Import run_codex_from_md dai "scripts"
scripts_path = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))
try:
    from run_selfmission import run_codex_from_md
except ImportError as e:
    def run_codex_from_md(path: str) -> str:
        return f"⚠️ Errore: run_selfmission non disponibile ({e})"

# ✅ Lettura e scrittura permanente dei file di Mercurius∞
BASE_PATH = Path(__file__).resolve().parent.parent  # Root del progetto

# 🧠 Avvia FastAPI
app = FastAPI(title="JOSCH Bridge")
start_time = time.time()

# ---------- MODELLI ----------
class CommandRequest(BaseModel):
    command: str
    mode: str = "cmd"  # cmd | powershell | python


# ---------- HEALTH ----------
@app.get("/ping")
def ping():
    return {"status": "online", "uptime": f"{int(time.time() - start_time)}s"}


# ---------- FILE-SYSTEM API ----------
@app.get("/list_files")
def list_files(subpath: str = ""):
    """Restituisce la lista di file .py sotto BASE_PATH/subpath."""
    path = BASE_PATH / subpath
    if not path.exists():
        return {"error": "Path non trovato."}
    return [
        str(p.relative_to(BASE_PATH))
        for p in path.rglob("*.py")
        if p.is_file()
    ]


@app.get("/read_file")
def read_file(filepath: str):
    """Legge e restituisce il contenuto UTF-8 di un file relativo a BASE_PATH."""
    full_path = BASE_PATH / filepath
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File non trovato")
    return {"content": full_path.read_text(encoding="utf-8")}


@app.post("/write_file")
def write_file(filepath: str, content: str):
    """
    Crea/sovrascrive un file.  
    Crea le cartelle intermedie quando assenti.
    """
    full_path = BASE_PATH / filepath
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"status": "OK", "written_to": str(full_path)}


# ---------- COMANDI REMOTI ----------
@app.post("/cmd")
def run_command(req: CommandRequest):
    try:
        # 🔁 SELF_MISSION da file .md
        if req.command.strip().startswith("#SELF_MISSION:"):
            path = req.command.split(":", 1)[1].strip()
            output = run_codex_from_md(path)
            return {"returncode": 0, "stdout": output, "stderr": ""}

        # 🧾 Shell / PowerShell / Python runtime
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


# ---------- WEBHOOK TRADINGVIEW ----------
@app.post("/tvhook")
def tvhook(payload: dict):
    """📡 Riceve comandi da TradingView tramite n8n."""
    file_path = os.path.join("logs", "tv_signal.json")
    os.makedirs("logs", exist_ok=True)
    try:
        entries = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                entries = json.load(f)
        if not isinstance(entries, list):
            entries = []
        entries.append({"timestamp": time.time(), "data": payload})
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Errore salvataggio segnale: {exc}")
    try:
        from trading.tv_watcher import handle_tv_signal
        handle_tv_signal(payload)
    except Exception:
        pass
    return {"status": "ok"}


# ---------- HELPER ----------
def send_command_to_pc(command: str, mode: str = "cmd", base_url: str = "http://localhost:3020") -> dict:
    """📨 Invia un comando al bridge JOSCH e restituisce la risposta JSON."""
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
