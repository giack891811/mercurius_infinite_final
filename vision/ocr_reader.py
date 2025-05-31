# vision/ocr_reader.py

"""
Modulo: ocr_reader.py
Descrizione: Estrazione testi da immagini o webcam tramite OCR (Tesseract).
Supporta JPEG, PNG, flussi video.
"""

import pytesseract
import cv2


class OCRReader:
    def __init__(self):
        pass

    def read_text_from_image(self, path: str) -> str:
        img = cv2.imread(path)
        return pytesseract.image_to_string(img, lang="ita+eng")

    def read_from_camera(self, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            text = pytesseract.image_to_string(frame)
            print(f"[OCR] {text.strip()}")
            cv2.imshow("OCR Live", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
