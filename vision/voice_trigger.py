# voice/voice_trigger.py

"""
Modulo: voice_trigger.py
Descrizione: Attivazione vocale tramite parola chiave "Hey Mercurius" utilizzando STT.
"""

import speech_recognition as sr


def listen_for_trigger(trigger_word: str = "hey mercurius") -> bool:
    """
    Ascolta il microfono per attivazione vocale.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎙️ Ascolto in corso... (parola chiave: 'Hey Mercurius')")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"🗣️ Rilevato: {text}")
        return trigger_word in text
    except sr.UnknownValueError:
        print("⚠️ Audio non riconosciuto.")
    except sr.RequestError:
        print("❌ Errore nel servizio di riconoscimento.")

    return False
