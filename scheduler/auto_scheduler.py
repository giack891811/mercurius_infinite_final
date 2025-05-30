"""
auto_scheduler.py
=================
Modulo per programmazione automatica di esecuzioni trading e test.

Basato su threading + pianificazione in tempo reale:
- task ciclici
- esecuzioni ritardate
- notifiche pianificate
"""

import threading
import time
from datetime import datetime, timedelta


class AutoScheduler:
    def __init__(self):
        self.tasks = []

    def schedule_task(self, task_func, delay_sec=5, repeat=False, interval_sec=60, name=None):
        """Programma un task con delay e ripetizione opzionale."""
        task = {
            "name": name or task_func.__name__,
            "function": task_func,
            "delay": delay_sec,
            "repeat": repeat,
            "interval": interval_sec,
            "next_run": datetime.now() + timedelta(seconds=delay_sec)
        }
        self.tasks.append(task)

    def run(self):
        """Avvia il ciclo continuo di pianificazione."""
        def loop():
            while True:
                now = datetime.now()
                for task in self.tasks:
                    if now >= task["next_run"]:
                        try:
                            print(f"🕒 Esecuzione task: {task['name']}")
                            task["function"]()
                        except Exception as e:
                            print(f"❌ Errore nel task {task['name']}: {e}")
                        if task["repeat"]:
                            task["next_run"] = now + timedelta(seconds=task["interval"])
                        else:
                            self.tasks.remove(task)
                time.sleep(1)

        threading.Thread(target=loop, daemon=True).start()

    def list_tasks(self):
        """Lista dei task programmati."""
        return [(t["name"], t["next_run"]) for t in self.tasks]

    def clear(self):
        self.tasks.clear()
