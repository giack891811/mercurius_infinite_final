"""teacher_mode.py
Gestisce la modalità di assistenza didattica continua.
"""
from __future__ import annotations

import threading
import time

from utils.logger import setup_logger
from modules.vision.eye_agent import EyeAgent
from modules.vision.vision_analyzer import VisionAnalyzer
from modules.didactic_reasoner import DidacticReasoner
from modules.voice_feedback import speak_feedback

logger = setup_logger(__name__)


class TeacherMode:
    """Modalità tutor sempre attiva."""

    def __init__(self) -> None:
        self.eye = EyeAgent()
        self.analyzer = VisionAnalyzer()
        self.reasoner = DidacticReasoner()
        self.active = False
        self._thread: threading.Thread | None = None

    def toggle(self, state: bool) -> None:
        logger.info("Teacher Mode %s", "ON" if state else "OFF")
        self.active = state
        if state and (self._thread is None or not self._thread.is_alive()):
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def _loop(self) -> None:
        while self.active:
            frame = self.eye.capture_frame()
            if frame is not None:
                text = self.analyzer.analyze_frame(frame)
                feedback = self.reasoner.generate_feedback(text)
                if feedback:
                    speak_feedback(feedback)
            time.sleep(5)
