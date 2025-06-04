"""Interactive voice loop using Whisper STT and gTTS."""
import os
from modules.voice_bridge.speech_to_text import WhisperSTT
from modules.voice_bridge.text_to_speech import TextToSpeech


def start_listening():
    stt = WhisperSTT()
    tts = TextToSpeech()
    print("[VOICE] Say 'exit' to stop. Provide path to .wav file for recognition.")
    while True:
        path = input("Audio file> ")
        if path.strip().lower() == "exit":
            break
        if not os.path.exists(path):
            print("File not found")
            continue
        text = stt.transcribe(path)
        print("[STT]", text)
        tts.speak(text)
