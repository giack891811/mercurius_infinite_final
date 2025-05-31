# vision/object_vision.py

"""
Modulo: object_vision.py
Descrizione: Riconoscimento oggetti in tempo reale da webcam con YOLOv8.
"""

import cv2
import supervision as sv
from ultralytics import YOLO


class ObjectVision:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=1, text_scale=0.5)

    def start_detection(self, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError("Camera non accessibile.")

        print("🎥 Avvio rilevamento oggetti YOLOv8... Premi 'q' per uscire.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(results)
            labels = [f"{c} {s:.2f}" for c, s in zip(results.names.values(), results.boxes.conf.cpu().numpy())]

            annotated = self.box_annotator.annotate(scene=frame, detections=detections, labels=labels)
            cv2.imshow("Mercurius∞ Vision", annotated)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def contextual_reaction(self, detected_items: list) -> str:
        if "person" in detected_items:
            return "👁️ Persona rilevata. Inizio monitoraggio ambientale."
        elif "keyboard" in detected_items:
            return "⌨️ Attività utente rilevata. Modalità lavoro attiva."
        else:
            return "🔍 Nessun oggetto prioritario rilevato."
