import speech_recognition as sr
from datetime import datetime
import random

def analyze_emotion_from_speech(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Ascolto... parla ora.")
        audio = recognizer.listen(source, timeout=timeout)

    try:
        text = recognizer.recognize_google(audio, language="it-IT")
        print(f"Testo riconosciuto: {text}")
        emotion = simulate_emotion_extraction(text)
        register_emotion_log(text, emotion)
        return emotion
    except sr.UnknownValueError:
        return "😐 Non ho capito..."
    except sr.RequestError as e:
        return f"Errore riconoscimento vocale: {e}"

def simulate_emotion_extraction(text):
    emozioni = ["felice", "stressato", "neutro", "incerto", "interessato"]
    return random.choice(emozioni)

def register_emotion_log(frase, emozione):
    log_path = "logs/self_monitoring/emotion_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] '{frase}' → EMOZIONE: {emozione}\n")