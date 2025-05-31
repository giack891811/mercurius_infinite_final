# deployment/task_scheduler.py

"""
Modulo: task_scheduler.py
Descrizione: Pianifica task periodici per Mercurius∞ (backup, aggiornamenti, invio telemetria).
"""

import schedule
import time
import threading
import logging


class TaskScheduler:
    def __init__(self):
        self.tasks = []
        logging.basicConfig(level=logging.INFO)

    def add_task(self, label: str, function, every_minutes: int = 1):
        schedule.every(every_minutes).minutes.do(self._wrapped_task, label, function)
        self.tasks.append((label, function))

    def _wrapped_task(self, label, func):
        try:
            result = func()
            logging.info(f"[Task OK] {label} ➜ {result}")
        except Exception as e:
            logging.error(f"[Task ERR] {label}: {e}")

    def start_loop(self):
        def runner():
            while True:
                schedule.run_pending()
                time.sleep(1)
        threading.Thread(target=runner, daemon=True).start()
