"""
Test: test_autonomia_cognitiva.py
Responsabilità: Verifica dei moduli self_reflection.py e learning.py
Autore: Mercurius∞ Engineer Mode
"""

import unittest
import os

from core.self_reflection import SelfReflection
from core.learning import ContinuousLearner

class TestAutonomiaCognitiva(unittest.TestCase):
    def setUp(self):
        self.test_reflection_path = "data/test_reflection_log.json"
        self.test_learning_path = "data/test_knowledge_base.json"

        if os.path.exists(self.test_reflection_path):
            os.remove(self.test_reflection_path)
        if os.path.exists(self.test_learning_path):
            os.remove(self.test_learning_path)

        self.reflection = SelfReflection(log_path=self.test_reflection_path)
        self.learner = ContinuousLearner(knowledge_path=self.test_learning_path)

    def test_reflection_logging(self):
        context = {"error": "Timeout"}
        result = self.reflection.evaluate_action("Scan Area", "No response", False, context)
        self.assertIn("insight", result)
        self.assertFalse(result["success"])

        log = self.reflection.logger.load_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["action"], "Scan Area")

    def test_reflection_summary(self):
        self.reflection.evaluate_action("Init Sequence", "OK", True, {})
        self.reflection.evaluate_action("Connect API", "403 Forbidden", False, {"error": "Auth failed"})
        summary = self.reflection.summarize_reflections()
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["successes"], 1)
        self.assertEqual(summary["failures"], 1)

    def test_learning_mechanism(self):
        context = {"sensor": "IR"}
        insight = self.learner.learn_from_experience("Move Forward", "Success", True, context)
        self.assertTrue("Esperienza positiva" in insight["insight"])

        data = self.learner.kb.load()
        self.assertEqual(len(data), 1)

    def test_learning_statistics(self):
        self.learner.learn_from_experience("Pick Object", "Failed", False, {"error": "gripper jam"})
        self.learner.learn_from_experience("Drop Object", "OK", True, {})
        stats = self.learner.stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["successes"], 1)
        self.assertEqual(stats["failures"], 1)

    def tearDown(self):
        if os.path.exists(self.test_reflection_path):
            os.remove(self.test_reflection_path)
        if os.path.exists(self.test_learning_path):
            os.remove(self.test_learning_path)

if __name__ == "__main__":
    unittest.main()
