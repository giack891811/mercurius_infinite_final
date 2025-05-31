# vision/capture.py

"""
Modulo: capture.py
Descrizione: Acquisizione video da IP Webcam per Mercurius∞. Utilizza OpenCV per estrarre frame in tempo reale.
"""

import cv2
import numpy as np
from typing import Optional


def get_frame_from_ip(ip_url: str) -> Optional[np.ndarray]:
    """
    Recupera un frame dall'indirizzo IP di una webcam.
    """
    cap = cv2.VideoCapture(ip_url)
    if not cap.isOpened():
        print("❌ Impossibile connettersi alla webcam IP.")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("⚠️ Nessun frame catturato.")
        return None

    return frame
