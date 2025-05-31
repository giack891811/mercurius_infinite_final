# vision/image_vision.py

"""
Modulo: image_vision.py
Descrizione: Analisi di immagini statiche con OCR per l'estrazione di testo e concetti visuali.
Usa pytesseract per lettura OCR e OpenCV per preprocessing.
"""

import pytesseract
import cv2
import numpy as np
from typing import List


class ImageVision:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Aggiorna se necessario

    def read_text_from_image(self, image_path: str) -> str:
        """
        Estrae il testo da un'immagine tramite OCR.
        """
        try:
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            return text.strip()
        except Exception as e:
            return f"[ERRORE OCR]: {e}"

    def extract_labels(self, image_path: str) -> List[str]:
        """
        Placeholder per estensione con modello YOLO/Vision per rilevamento oggetti.
        """
        return ["[analisi visiva non implementata]"]
