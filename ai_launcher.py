import subprocess
import requests
import time
import os
from typing import List

from utils.logger import get_file_logger

LOG_FILE = os.path.join("logs", "service_launcher.log")
logger = get_file_logger("ServiceLauncher", LOG_FILE)

def is_service_running(url: str, timeout: int = 2) -> bool:
    """Check if a service responds on the given URL."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code in [200, 401, 403]
    except requests.exceptions.RequestException:
        return False

def launch_service(name: str, url: str, command: List[str], delay: int = 5, retries: int = 5) -> None:
    """Ensure that a service is running, otherwise try to start it."""
    if is_service_running(url):
        logger.info(f"{name} è già attivo su {url}")
        return

    logger.info(f"Avvio {name}: {' '.join(command)}")
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for _ in range(retries):
        if is_service_running(url):
            logger.info(f"{name} avviato correttamente.")
            return
        time.sleep(delay)

    logger.error(f"{name} non risponde su {url}")

def ensure_ai_online():
    launch_service("Ollama", "http://localhost:11434", ["ollama", "serve"], delay=3)
    launch_service("Ollama3", "http://localhost:11434/api/tags", ["ollama", "run", "llama3"], delay=3)
    launch_service("AZR", "http://localhost:4010/introspect", ["python", "azr_server.py"], delay=2)
    launch_service("JOSCH", "http://localhost:3020/ping", ["python", "josch_server.py"], delay=2)
    launch_service("n8n", "http://localhost:5678", ["n8n", "start"], delay=4)

if __name__ == "__main__":
    ensure_ai_online()
