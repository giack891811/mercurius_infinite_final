"""
Test: test_supervisione.py
Responsabilità: Verifica comportamento dei moduli di supervisione e telemetria
Autore: Mercurius∞ Engineer Mode
"""

import unittest
from modules.supervisor import Supervisor
from utils.telemetry import Telemetry


class TestSupervisor(unittest.TestCase):

    def setUp(self):
        self.supervisor = Supervisor()

    def test_observe_and_report(self):
        self.supervisor.observe("scan", "ok", True, {"sensor": "lidar"})
        self.supervisor.observe("move", "collision", False, {"speed": "fast"})

        report = self.supervisor.performance_report()
        self.assertEqual(report["actions_total"], 2)
        self.assertEqual(report["successes"], 1)
        self.assertEqual(report["failures"], 1)
        self.assertGreaterEqual(report["success_rate"], 0.0)

    def test_last_actions(self):
        self.supervisor.observe("test1", "done", True, {})
        self.supervisor.observe("test2", "done", True, {})
        last = self.supervisor.last_actions(1)
        self.assertEqual(len(last), 1)
        self.assertEqual(last[0]["action"], "test2")


class TestTelemetry(unittest.TestCase):

    def test_system_info_keys(self):
        info = Telemetry.system_info()
        self.assertIn("platform", info)
        self.assertIn("memory_total_MB", info)

    def test_current_usage_structure(self):
        usage = Telemetry.current_usage()
        self.assertIn("cpu_percent", usage)
        self.assertIn("memory_used_MB", usage)

    def test_process_info(self):
        process = Telemetry.process_info()
        self.assertIn("pid", process)
        self.assertGreaterEqual(process["memory_MB"], 0)


if __name__ == "__main__":
    unittest.main()
