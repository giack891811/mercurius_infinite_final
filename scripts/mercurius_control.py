import argparse
import os
import subprocess
from pathlib import Path

PID_FILE = Path("mercurius.pid")


def start_system() -> None:
    if PID_FILE.exists():
        print("Mercurius∞ sembra già in esecuzione.")
        return
    process = subprocess.Popen(["python", "scripts/aion_boot.py"])
    PID_FILE.write_text(str(process.pid))
    print(f"Mercurius∞ avviato con PID {process.pid}")


def stop_system() -> None:
    if not PID_FILE.exists():
        print("Mercurius∞ non risulta attivo.")
        return
    pid = int(PID_FILE.read_text())
    try:
        os.kill(pid, 9)
        print("Mercurius∞ arrestato.")
    except ProcessLookupError:
        print("Processo non trovato.")
    PID_FILE.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gestione start/stop di Mercurius∞")
    parser.add_argument("action", choices=["start", "stop"], help="Azione da eseguire")
    args = parser.parse_args()
    if args.action == "start":
        start_system()
    else:
        stop_system()


if __name__ == "__main__":
    main()
