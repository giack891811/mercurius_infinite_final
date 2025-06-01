# trainer/trainer_trigger.py
"""
Modulo: trainer_trigger.py
Descrizione: Innesca SelfTrainer quando ci sono suff. nuove esperienze o in orario schedulato.
"""

import time
import threading
from pathlib import Path
from modules.experience.experience_memory import ExperienceMemory
from trainer.self_trainer import SelfTrainer

class TrainerTrigger:
    def __init__(self, exp_memory: ExperienceMemory, check_interval=600, min_new_exp=25):
        self.exp_memory = exp_memory
        self.check_interval = check_interval
        self.min_new_exp = min_new_exp
        self.trainer = SelfTrainer()
        self._last_count = 0
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            current_count = len(self.exp_memory.store.get_all())
            if current_count - self._last_count >= self.min_new_exp:
                print("🛠️ TrainerTrigger: Nuove esperienze sufficienti, avvio training...")
                advice = self.trainer.train_once(save_to=Path("logs/latest_strategy_advice.md"))
                print(f"📚 Suggerimenti strategici:\n{advice}\n")
                self._last_count = current_count
            time.sleep(self.check_interval)
