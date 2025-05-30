import cv2

def detect_from_stream(ip_camera_url="http://127.0.0.1:8080/video"):
    cap = cv2.VideoCapture(ip_camera_url)
    if not cap.isOpened():
        return "⚠️ Stream non accessibile"

    frame_count = 0
    while frame_count < 100:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Mercurius – Visione', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    return "✅ Analisi visiva completata"

def analyze_frame_logic(frame):
    # Simulazione logica per riconoscimento visivo
    height, width = frame.shape[:2]
    return {"dimensione": (width, height), "esempio": "Simulazione completata"}