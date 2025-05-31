# sensors/environment_analyzer.py

"""
Modulo: environment_analyzer.py
Descrizione: Analizza il livello di rumore ambientale e cambiamenti visivi dalla webcam.
Serve per attivare modalità silenziosa, reattiva o sicurezza.
"""

import cv2
import numpy as np
import sounddevice as sd


class EnvironmentAnalyzer:
    def __init__(self, camera_index=0):
        self.cam = cv2.VideoCapture(camera_index)

    def get_audio_level(self, duration=1) -> float:
        recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
        sd.wait()
        return float(np.abs(recording).mean())

    def detect_motion(self) -> str:
        ret, frame1 = self.cam.read()
        ret, frame2 = self.cam.read()
        if not ret:
            return "no_camera"

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        motion = np.sum(thresh) / 255
        if motion > 1000:
            return "movimento sospetto"
        return "nessun movimento"
