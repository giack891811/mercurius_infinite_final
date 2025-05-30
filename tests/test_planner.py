"""
Test: test_planner.py
Responsabilità: Verifica per ActionPlanner e GoalManager
Autore: Mercurius∞ Engineer Mode
"""

import unittest
from modules.planner import ActionPlanner
from modules.goal_manager import GoalManager


class TestActionPlanner(unittest.TestCase):

    def setUp(self):
        self.planner = ActionPlanner()

    def test_generate_plan_for_known_goal(self):
        plan = self.planner.generate_plan("analizza_ambiente", {})
        self.assertGreater(len(plan), 0)
        self.assertTrue(all("action" in step for step in plan))

    def test_validate_plan(self):
        plan = self.planner.generate_plan("interagisci_utente", {})
        self.assertTrue(self.planner.validate_plan(plan))

    def test_describe_plan(self):
        plan = self.planner.generate_plan("raggiungi_destinazione", {"destinazione": "Base"})
        description = self.planner.describe_plan(plan)
        self.assertIn("calcola_percorso", description)
        self.assertIn("Base", description)

    def test_plan_summary(self):
        self.planner.generate_plan("analizza_ambiente", {})
        summary = self.planner.plan_summary()
        self.assertIn("step_count", summary)
        self.assertGreater(summary["step_count"], 0)


class TestGoalManager(unittest.TestCase):

    def setUp(self):
        self.manager = GoalManager()

    def test_add_and_sort_goals(self):
        self.manager.add_goal("goal1", priority=2)
        self.manager.add_goal("goal2", priority=5)
        top = self.manager.get_next_goal()
        self.assertEqual(top.name, "goal2")

    def test_goal_status_transition(self):
        self.manager.add_goal("goalX")
        g = self.manager.get_next_goal()
        self.assertEqual(g.status, "active")
        self.manager.complete_goal("goalX")
        all_goals = self.manager.all_goals()
        self.assertEqual(all_goals[0]["status"], "completed")

    def test_active_and_pending_filter(self):
        self.manager.add_goal("goalY", priority=1)
        self.manager.add_goal("goalZ", priority=2)
        self.manager.get_next_goal()
        active = self.manager.active_goals()
        pending = self.manager.pending_goals()
        self.assertEqual(len(active), 1)
        self.assertEqual(len(pending), 1)


if __name__ == "__main__":
    unittest.main()
