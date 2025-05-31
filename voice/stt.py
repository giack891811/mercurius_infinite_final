# voice/stt.py

"""
Modulo: stt.py
Descrizione: Riconoscimento vocale da microfono in testo utilizzando SpeechRecognition (Google STT).
"""

import speech_recognition as sr


def transcribe_audio() -> str:
    """
    Converte l'audio acquisito da microfono in testo.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎧 In ascolto...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="it-IT")
        print(f"📝 Riconosciuto: {text}")
        return text
    except sr.UnknownValueError:
        return "[Voce non riconosciuta]"
    except sr.RequestError:
        return "[Errore nel riconoscimento vocale]"
