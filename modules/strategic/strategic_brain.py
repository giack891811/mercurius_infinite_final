"""Strategic Brain module integrating gpt_engineer with Mercurius∞.
"""
from pathlib import Path
from typing import List

from modules.goal_manager import GoalManager, Goal
from modules.gpt_engineer_wrapper import GPTEngineerWrapper
from modules.llm.azr_reasoner import AZRAgent
from orchestrator.genesis_orchestrator import GenesisOrchestrator


class StrategicBrain:
    """High level manager that routes goals to LLMs and falls back to GPT-Engineer."""

    def __init__(self, workspace: str = "strategic_projects") -> None:
        self.goal_manager = GoalManager()
        self.orchestrator = GenesisOrchestrator()
        self.validator = AZRAgent()
        self.builder = GPTEngineerWrapper(project_path=workspace)
        Path(workspace).mkdir(exist_ok=True)

    def load_goals(self, goals_path: str) -> None:
        """Load goals from a text file."""
        path = Path(goals_path)
        if not path.exists():
            return
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                self.goal_manager.add_goal(line)

    def execute_goal(self, goal: Goal) -> str:
        """Process a single goal using the orchestrator and fallback with GPT-Engineer."""
        result = self.orchestrator.route_task(goal.name)
        analysis = self.validator.analyze(result.get("response", ""))
        if isinstance(analysis, str) and analysis.startswith("❌"):
            # invalid response: trigger GPT-Engineer
            return self.builder.generate_project(goal.name)
        return result.get("response", "")

    def run(self) -> List[str]:
        """Run through all pending goals and return list of outputs."""
        outputs = []
        while True:
            next_goal = self.goal_manager.get_next_goal()
            if not next_goal:
                break
            output = self.execute_goal(next_goal)
            outputs.append(output)
            self.goal_manager.complete_goal(next_goal.name)
        return outputs
