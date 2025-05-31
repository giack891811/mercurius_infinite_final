# learning/video_learner.py

"""
Modulo: video_learner.py
Descrizione: Apprendimento da contenuti video (es. YouTube).
Estrae audio → trascrive con Whisper → restituisce sintesi concettuale.
Supporta fallback se i moduli non sono disponibili.
"""

import os
import tempfile

# ─── Import Condizionali ──────────────────────────────────────────────
try:
    from pytube import YouTube
    import whisper
    MODULES_AVAILABLE = True
except ImportError:
    YouTube = None
    whisper = None
    MODULES_AVAILABLE = False


class VideoLearner:
    def __init__(self, model_name="large-v3"):
        if MODULES_AVAILABLE and whisper:
            self.model = whisper.load_model(model_name)
        else:
            self.model = None

    def download_audio(self, url: str) -> str:
        """
        Scarica solo l'audio da un video YouTube in formato MP4.
        """
        if not MODULES_AVAILABLE or YouTube is None:
            return "[❌ pytube non disponibile]"
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            out_path = tempfile.mktemp(suffix=".mp4")
            stream.download(filename=out_path)
            return out_path
        except Exception as e:
            return f"[❌ Errore download audio]: {e}"

    def transcribe_audio(self, file_path: str) -> str:
        """
        Trascrive un file audio tramite Whisper.
        """
        if not self.model:
            return "[❌ Whisper non disponibile]"
        try:
            result = self.model.transcribe(file_path, language="it")
            return result.get("text", "[nessuna trascrizione]")
        except Exception as e:
            return f"[❌ Errore Whisper]: {e}"

    def extract_insights_from_video(self, url: str) -> str:
        """
        Processo completo: download → trascrizione.
        """
        if not MODULES_AVAILABLE:
            return "[❌ Moduli mancanti: pytube, whisper]"

        audio_path = self.download_audio(url)
        if audio_path.startswith("[❌"):
            return audio_path

        return self.transcribe_audio(audio_path)
