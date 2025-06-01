"""
Modulo: video_pipeline.py
Descrizione: Gestione realistica della pipeline video con placeholder di fallback.
Autore: Mercurius∞ AI Engineer
"""

import cv2
import threading

class VideoPipeline:
    def __init__(self, source=0, use_placeholder=False):
        """
        source: indice webcam o percorso file
        use_placeholder: se True usa il placeholder semplice senza OpenCV
        """
        self.source = source
        self.use_placeholder = use_placeholder
        self.active = False
        self.capture_thread = None

    def _process_frame(self, frame):
        """Elabora il frame video (placeholder per elaborazioni future)."""
        print("[VISION] Frame catturato.")
        return frame

    def _capture_loop(self):
        """Ciclo continuo di cattura video con OpenCV."""
        cap = cv2.VideoCapture(self.source)
        if not cap.isOpened():
            print("[VISION] Impossibile aprire la sorgente video.")
            return

        while self.active:
            ret, frame = cap.read()
            if not ret:
                break
            self._process_frame(frame)
        cap.release()
        print("[VISION] Video terminato.")

    def start(self):
        """Avvia la pipeline video (reale o placeholder)."""
        if self.active:
            return
        print(f"[VISION] Avvio pipeline video su '{self.source}' " + 
              ("(placeholder)" if self.use_placeholder else "(reale)"))
        self.active = True
        if self.use_placeholder:
            print(f"📹 VideoPipeline avviata su '{self.source}' (placeholder)")
        else:
            self.capture_thread = threading.Thread(target=self._capture_loop)
            self.capture_thread.start()

    def stop(self):
        """Arresta la pipeline video."""
        if not self.active:
            return
        self.active = False
        if self.capture_thread:
            self.capture_thread.join()
        print("🛑 Pipeline video fermata")

# Esempio di esecuzione diretta
if __name__ == "__main__":
    vp = VideoPipeline(source=0, use_placeholder=False)
    vp.start()
    import time
    time.sleep(5)
    vp.stop()
