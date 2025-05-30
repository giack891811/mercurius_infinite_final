import cv2

def start_note10_sync(ip_camera_url="http://192.168.0.10:8080/video",
                      use_hotword=True,
                      request_qr_if_fail=True):
    print("📲 Avvio sincronizzazione con Note10+...")

    try:
        cap = cv2.VideoCapture(ip_camera_url)
        if not cap.isOpened():
            raise ConnectionError("⚠️ Impossibile connettersi alla camera IP")

        print("✅ Stream ricevuto. Avvio visione artificiale...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Note10+ Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"❌ Errore connessione: {e}")
        if request_qr_if_fail:
            print("📸 Generazione QR code per pairing alternativo (simulazione)")