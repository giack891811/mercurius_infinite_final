from modules.voice_bridge.audio_interface import AudioInterface

def test_audio_initialization():
    audio = AudioInterface()
    audio.initialize()
    assert audio.microphone_ready
    assert audio.tts_ready

def test_audio_listen_and_speak():
    audio = AudioInterface()
    audio.initialize()
    spoken = audio.listen()
    assert isinstance(spoken, str)
    assert "simulato" in spoken
    response = audio.speak("Messaggio di test")
    assert response is None  # La funzione speak stampa ma non ritorna nulla
