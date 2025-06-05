import subprocess
import requests
import time
import os

def is_service_running(url: str, timeout: int = 2) -> bool:
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code in [200, 401, 403]
    except requests.exceptions.RequestException:
        return False

def launch_service(name: str, url: str, command: list, delay: int = 5):
    if not is_service_running(url):
        print(f"🔄 {name} non attivo. Avvio in corso...")
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(delay)
    else:
        print(f"✅ {name} è già attivo.")

def ensure_ai_online():
    launch_service("Ollama", "http://localhost:11434", ["ollama", "serve"], delay=3)
    launch_service("AZR", "http://localhost:4010/introspect", ["python", "azr_server.py"], delay=2)
    launch_service("JOSCH", "http://localhost:3020/ping", ["python", "josch_server.py"], delay=2)
    launch_service("n8n", "http://localhost:5678", ["n8n", "start"], delay=4)

if __name__ == "__main__":
    ensure_ai_online()
