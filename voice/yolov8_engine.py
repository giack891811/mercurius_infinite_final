# vision/yolov8_engine.py

"""
Modulo: yolov8_engine.py
Descrizione: Riconoscimento in tempo reale di oggetti, volti e gesti con YOLOv8.
Supporta flussi da webcam o video file.
"""

import cv2
from ultralytics import YOLO


class VisionAI:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect_from_image(self, image_path: str) -> list:
        results = self.model(image_path)
        return results[0].names

    def detect_from_webcam(self, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            results = self.model(frame)
            annotated = results[0].plot()
            cv2.imshow("Mercurius Vision", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
