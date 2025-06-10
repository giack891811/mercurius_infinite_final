"""
eye_agent.py
Gestisce la visione artificiale in tempo reale con funzioni di screenshot.
"""

from pathlib import Path
from typing import Optional, TYPE_CHECKING, Any

try:
    import cv2
except Exception:  # pragma: no cover - cv2 may not be available
    cv2 = None

if TYPE_CHECKING:
    import cv2  # solo per type hinting statico
    MatType = Optional["cv2.typing.MatLike"]
else:
    MatType = Optional[Any]

from utils.logger import setup_logger
from modules.stream_vision.video_pipeline import VideoPipeline
from vision.ocr_module import extract_text_from_image

logger = setup_logger(__name__)


class EyeAgent:
    """Interfaccia semplificata per accesso a webcam o sorgenti video."""

    def __init__(self, source: int | str = 0, use_placeholder: bool = False):
        self.pipeline = VideoPipeline(source=source, use_placeholder=use_placeholder)
        self.source = source

    def capture_frame(self) -> MatType:
        """Restituisce un singolo frame dalla sorgente."""
        if cv2 is None:
            logger.warning("cv2 non disponibile; impossibile catturare frame")
            return None
        cap = cv2.VideoCapture(self.source)
        ret, frame = cap.read()
        cap.release()
        if ret:
            logger.debug("[EYE] Frame catturato")
            return frame
        logger.error("[EYE] Nessun frame catturato")
        return None

    def screenshot(self, path: str = "logs/eye/screenshot.jpg") -> Optional[str]:
        """Salva un singolo screenshot."""
        frame = self.capture_frame()
        if frame is None:
            return None
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(path, frame)
        logger.info(f"[EYE] Screenshot salvato in {path}")
        return path

    def ocr_snapshot(self, path: str = "logs/eye/ocr_shot.jpg") -> str:
        """Cattura screenshot e restituisce testo OCR."""
        img_path = self.screenshot(path)
        if not img_path:
            return ""
        return extract_text_from_image(img_path)

    def start_stream(self):
        """Avvia la pipeline video in streaming."""
        self.pipeline.start()

    def stop_stream(self):
        """Ferma la pipeline video."""
        self.pipeline.stop()
