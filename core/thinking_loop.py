"""thinking_loop.py
Loop di pensiero continuo e autonomo per Mercurius∞.
"""
from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import List

import yaml

try:
    import requests
    import arxiv  # type: ignore
    import wikipedia  # type: ignore
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover - alcuni moduli opzionali possono mancare
    requests = None
    arxiv = None
    wikipedia = None
    BeautifulSoup = None

try:
    from utils.logger import setup_logger
except Exception:  # pragma: no cover - fallback semplice
    def setup_logger(name: str = "ThinkingLoop"):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)
        return logger


LOG_PATH = Path("logs/thinking_feed.md")
LOG_PATH.parent.mkdir(exist_ok=True)


class ThinkingLoop:
    """Esegue ricerche e genera insight senza bloccare gli agenti."""

    def __init__(self, config_file: str = "config/genesis_config.yaml") -> None:
        self.config_file = Path(config_file)
        self.enabled = True
        self._load_config()
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.logger = setup_logger("ThinkingLoop")
        self.last_pos = 0
        self.interval = 300  # 5 minuti
        self.response_timeout = 3

    def _load_config(self) -> None:
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
            self.enabled = cfg.get("thinking_enabled", True)

    def start(self) -> None:
        if not self.enabled:
            self.logger.info("Thinking loop disabilitato da config.")
            return
        if not self.thread.is_alive():
            self.thread.start()
            self.logger.info("Thinking loop avviato.")

    def stop(self) -> None:
        self._stop.set()
        if self.thread.is_alive():
            self.thread.join(timeout=1)

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self._analyse_logs()
                self._perform_research()
            except Exception as exc:  # pragma: no cover - logga errori inattesi
                self.logger.error("Errore thinking loop: %s", exc)
            for _ in range(self.interval):
                if self._stop.is_set():
                    break
                time.sleep(1)

    def _write_feed(self, text: str) -> None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"- {timestamp} {text}\n")

    def _analyse_logs(self) -> None:
        log_file = Path("logs/system.log")
        if not log_file.exists():
            return
        with open(log_file, "r", encoding="utf-8") as f:
            f.seek(self.last_pos)
            data = f.read()
            self.last_pos = f.tell()
        if data:
            lines = data.strip().splitlines()[-5:]
            if lines:
                self._write_feed("Nuovi log:\n" + "\n".join(f"  {l}" for l in lines))

    def _perform_research(self) -> None:
        insights: List[str] = []
        insights += self._fetch_arxiv()
        insights += self._fetch_github()
        insights += self._fetch_huggingface()
        insights += self._fetch_wikipedia()
        for ins in insights:
            self._write_feed(ins)

    def _fetch_arxiv(self) -> List[str]:
        if not arxiv:
            return []
        try:
            search = arxiv.Search(query="machine learning", max_results=1, sort_by=arxiv.SortCriterion.SubmittedDate)
            result = next(search.results(), None)
            if result:
                return [f"arXiv: {result.title.strip()} – {result.entry_id}"]
        except Exception as exc:  # pragma: no cover
            self.logger.warning("arXiv errore: %s", exc)
        return []

    def _fetch_github(self) -> List[str]:
        if not requests or not BeautifulSoup:
            return []
        url = "https://github.com/trending"
        try:
            resp = requests.get(url, timeout=5)
            if resp.ok:
                soup = BeautifulSoup(resp.text, "html.parser")
                repo = soup.select_one("article h1 a")
                if repo:
                    return [f"GitHub trending: {repo.text.strip()}"]
        except Exception as exc:  # pragma: no cover
            self.logger.warning("GitHub trending fallito: %s", exc)
        return []

    def _fetch_huggingface(self) -> List[str]:
        if not requests:
            return []
        url = "https://huggingface.co/api/models?sort=downloads&limit=1"
        try:
            resp = requests.get(url, timeout=5)
            if resp.ok:
                data = resp.json()
                if data:
                    return [f"HF model più scaricato: {data[0].get('modelId')}"]
        except Exception as exc:  # pragma: no cover
            self.logger.warning("HuggingFace API fallita: %s", exc)
        return []

    def _fetch_wikipedia(self) -> List[str]:
        if not wikipedia:
            return []
        try:
            summary = wikipedia.summary("Artificial intelligence", sentences=1)
            return [f"Wiki AI: {summary}"]
        except Exception as exc:  # pragma: no cover
            self.logger.warning("Wikipedia errore: %s", exc)
        return []

    def ask_mercurius(self, prompt: str) -> str:
        """Invia una richiesta a Mercurius∞ con timeout e fallback."""
        if not requests:
            return ""
        url = "http://localhost:8000/ask"
        try:
            resp = requests.post(url, json={"prompt": prompt}, timeout=self.response_timeout)
            if resp.ok:
                return resp.json().get("response", "")
        except Exception:  # pragma: no cover - log non necessario
            pass
        self._write_feed("Modalità fallback: sto elaborando, signore...")
        threading.Thread(target=self._perform_research, daemon=True).start()
        return "Sto elaborando, signore..."


def start_thinking_loop() -> ThinkingLoop:
    """Helper per avviare rapidamente il thinking loop."""
    loop = ThinkingLoop()
    loop.start()
    return loop

if __name__ == "__main__":  # pragma: no cover - avvio manuale
    start_thinking_loop()
    while True:
        time.sleep(1)

