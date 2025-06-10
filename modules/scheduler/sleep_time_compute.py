"""sleep_time_compute.py
Esecuzione di task di ottimizzazione durante i periodi di inattivita'.
Include auto-tuning del codice e salvataggio di suggerimenti.
"""

import time
from utils.logger import setup_logger
from core.self_tuner import SelfTuner

logger = setup_logger(__name__)


class SleepTimeCompute:
    """Scheduler semplificato per calcoli offline."""

    def __init__(self, interval: int = 3600):
        self.interval = interval
        self.active = False
        self.tuner = SelfTuner()

    def execute_tasks(self):
        """Placeholder per attivita' di ottimizzazione notturna."""
        logger.debug("[SLEEP] Esecuzione routine di ottimizzazione")
        try:
            self.tuner.run_autoanalysis()
        except Exception as exc:  # pragma: no cover
            logger.error("Errore ottimizzazione sleep: %s", exc)

    def run(self):
        logger.info("[SLEEP] Avvio SleepTimeCompute")
        self.active = True
        while self.active:
            self.execute_tasks()
            time.sleep(self.interval)

    def stop(self):
        self.active = False
        logger.info("[SLEEP] SleepTimeCompute terminato")
