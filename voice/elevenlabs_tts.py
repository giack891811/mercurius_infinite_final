# voice/elevenlabs_tts.py

"""
Modulo: elevenlabs_tts.py
Descrizione: Voce naturale con API ElevenLabs – stile Jarvis.
"""

import requests
import os

class ElevenLabsTTS:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")

    def speak(self, text: str, voice_id="EXAVITQu4vr4xnSDxMaL"):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        json_data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        response = requests.post(url, json=json_data, headers=headers)
        with open("output_11labs.wav", "wb") as f:
            f.write(response.content)
