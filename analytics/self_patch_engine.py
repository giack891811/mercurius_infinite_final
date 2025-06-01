# analytics/self_patch_engine.py
"""
Modulo: self_patch_engine.py
Descrizione: Genera una patch git e crea automaticamente un branch+commit con i
suggerimenti di NeuroOptimizer.
"""

import subprocess
from pathlib import Path
from typing import Optional
from analytics.neuro_optimizer import NeuroOptimizer
from analytics.behavior_logger import BehaviorLogger

class SelfPatchEngine:
    def __init__(self, repo_root: str = "."):
        self.root = Path(repo_root)
        self.optimizer = NeuroOptimizer()
        self.logger = BehaviorLogger()

    def _git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)

    def apply_patch(self) -> Optional[str]:
        suggestion = self.optimizer.suggest_patch()
        if not suggestion:
            print("Nessuna patch suggerita.")
            return None
        path = Path(suggestion["path"])
        branch = f"auto_patch_{path.stem}"
        self._git("checkout", "-B", branch)
        path.write_text(suggestion["code"], encoding="utf-8")
        self._git("add", str(path))
        self._git("commit", "-m", f"🤖 Auto-patch {path.name} (NeuroOptimizer)")
        self.logger.log("auto_patch", {"path": suggestion["path"]})
        print(f"✅ Patch applicata su branch {branch}")
        return branch
