"""vision_analyzer.py
Analizza frame o immagini e restituisce testo descrittivo.
"""
from __future__ import annotations

from typing import Optional

try:
    import cv2
except Exception:  # pragma: no cover - cv2 optional
    cv2 = None

try:
    import pytesseract
except Exception:  # pragma: no cover - tesseract optional
    pytesseract = None

from utils.logger import setup_logger

logger = setup_logger(__name__)


class VisionAnalyzer:
    """Interpretazione base di screenshot o frame."""

    def analyze_frame(self, frame) -> str:
        if pytesseract and frame is not None and cv2 is not None:
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray, lang="eng")
                return text.strip()
            except Exception as exc:  # pragma: no cover
                logger.error("OCR error: %s", exc)
        return "[VISION] Nessun contenuto riconosciuto"
