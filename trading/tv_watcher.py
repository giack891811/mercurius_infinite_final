import json
import os
import time
import threading

from utils.logger import setup_logger

TV_FILE = os.path.join("logs", "tv_signal.json")
LOG_FILE = os.path.join("logs", "tv_watcher.log")

logger = setup_logger("TVWatcher", LOG_FILE)


def handle_tv_signal(data: dict) -> None:
    """Gestisci un segnale TradingView appena ricevuto."""
    logger.info(f"Nuovo segnale TV: {data}")


def _read_signals():
    if not os.path.exists(TV_FILE):
        return []
    try:
        with open(TV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logger.error(f"Errore lettura {TV_FILE}: {exc}")
        return []


def watch_tv_signals(poll_interval: float = 5.0):
    logger.info("TV watcher avviato")
    last_len = 0
    while True:
        signals = _read_signals()
        if len(signals) > last_len:
            new = signals[last_len:]
            last_len = len(signals)
            for entry in new:
                try:
                    handle_tv_signal(entry.get("data", entry))
                except Exception as exc:
                    logger.error(f"Errore gestione segnale: {exc}")
        time.sleep(poll_interval)


def start_watcher():
    threading.Thread(target=watch_tv_signals, daemon=True).start()
