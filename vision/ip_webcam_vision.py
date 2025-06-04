"""YOLO based detection from IP webcam stream."""
import cv2
from vision.object_vision import ObjectVision

class IPWebcamVision(ObjectVision):
    def start_stream(self, ip_url: str):
        cap = cv2.VideoCapture(ip_url)
        if not cap.isOpened():
            raise RuntimeError("Cannot open IP camera")
        print("📡 Streaming IP webcam... press 'q' to quit")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = self.model(frame, verbose=False)[0]
            annotated = self.box_annotator.annotate(
                scene=frame,
                detections=results.boxes
            )
            cv2.imshow("Mercurius∞ IP Cam", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
