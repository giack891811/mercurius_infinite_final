"""
task_registry.py
================
Raccolta di task Mercurius∞ registrabili nello scheduler:
- simulazioni
- test
- azioni periodiche
"""

from core.pipeline_controller import PipelineController
from utils.config_loader import load_config

class TaskRegistry:
    def __init__(self):
        self.config = load_config("config/config.yaml")
        self.pipeline = PipelineController(self.config)

    def simulate_trading_session(self):
        """Task: esegue una sessione completa simulata."""
        print("▶️ Simulazione trading session")
        self.pipeline.run_batch_session()

    def multiple_sessions(self, count=3):
        """Task: n simulazioni."""
        print(f"▶️ Avvio {count} sessioni simulate")
        self.pipeline.simulate_multiple_sessions(n=count)

    def health_check(self):
        """Task diagnostico semplificato."""
        print("✅ Mercurius∞ pronto. Config:", self.config.get("symbols", []))
