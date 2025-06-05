"""mission_controller.py
Mission Controller per ciclo evolutivo multi-agente.
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Dict, Any

from orchestrator.genesis_orchestrator import GenesisOrchestrator
from orchestrator.autonomy_controller import AutonomyController
from modules.llm.azr_reasoner import AZRAgent
from modules.gpt_engineer_wrapper import GPTEngineerWrapper
from modules.sandbox_executor.secure_executor import SecureExecutor


class MissionController:
    """Gestisce il ciclo di self-questioning e auto-evoluzione."""

    def __init__(self, base_dir: str = "workspaces") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.genesis = GenesisOrchestrator()
        self.autonomy = AutonomyController()
        self.azr = AZRAgent()
        self.codex = GPTEngineerWrapper(project_path=str(self.base_dir))
        self.executor = SecureExecutor(timeout=5)
        self.workspaces: Dict[str, Dict[str, Any]] = {}
        self.log_file = Path("logs/mission_log.jsonl")
        self.log_file.parent.mkdir(exist_ok=True)

    # ------------------------------------------------------------------ #
    def create_workspace(self, name: str, prompt: str) -> Path:
        """Crea una cartella dedicata e salva il prompt."""
        path = self.base_dir / name
        path.mkdir(exist_ok=True)
        (path / "prompt.txt").write_text(prompt, encoding="utf-8")
        self.workspaces[name] = {"prompt": prompt, "path": path}
        self._log("workspace_created", {"name": name})
        return path

    # ------------------------------------------------------------------ #
    def _log(self, event: str, details: Dict[str, Any]) -> None:
        entry = {"event": event, "details": details}
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    # ------------------------------------------------------------------ #
    def run_cycle(self, name: str) -> None:
        """Esegue un ciclo evolutivo sul workspace indicato."""
        ws = self.workspaces.get(name)
        if not ws:
            return
        prompt = ws["prompt"]
        # 1. Reasoner: suggerimenti
        question = f"Come migliorare questo progetto? {prompt}"
        reason_resp = self.genesis.route_task(question)
        self.autonomy.process_experience("reason", "ok", True, {"workspace": name})

        # 2. AZR analizza la risposta
        analysis = self.azr.analyze(reason_resp.get("response", question))
        self.autonomy.process_experience("azr", analysis, True, {"workspace": name})

        # 3. Se AZR suggerisce problemi, genera patch con Codex
        if analysis.startswith("❌"):
            patch = self.codex.generate_project(prompt)
            (ws["path"] / "patch.log").write_text(patch, encoding="utf-8")
            self.autonomy.process_experience("codex_patch", patch, True, {"workspace": name})
            result = self.executor.execute(patch)
            (ws["path"] / "sandbox.log").write_text(str(result), encoding="utf-8")
        self._log("cycle_completed", {"workspace": name})


if __name__ == "__main__":
    mc = MissionController()
    ws = mc.create_workspace("demo", "Genera uno script di esempio")
    mc.run_cycle("demo")
