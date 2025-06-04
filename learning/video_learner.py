"""
Modulo: video_learner.py
Descrizione: Apprendimento da contenuti video e audio (YouTube, file locali).
Estrae audio → trascrive con Whisper → restituisce sintesi concettuale.
Supporta fallback se i moduli non sono disponibili.
Autore: Mercurius∞ AI Engineer
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
        Trascrive un file audio/video tramite Whisper.
        Accetta qualsiasi file locale audio o video.
        """
        if not self.model:
            return "[❌ Whisper non disponibile]"
        try:
            result = self.model.transcribe(file_path, language="it")
            return result.get("text", "[nessuna trascrizione]")
        except Exception as e:
            return f"[❌ Errore Whisper]: {e}"

    def extract_insights_from_video(self, source: str) -> str:
        """
        Processo completo:
        - Se input è un file locale esistente (MP4/MP3/etc.), trascrive direttamente.
        - Se input è un URL, scarica l'audio e poi trascrive.
        """
        if not MODULES_AVAILABLE:
            return "[❌ Moduli mancanti: pytube, whisper]"
        
        if os.path.exists(source):
            # Input è un file locale
            return self.transcribe_audio(source)
        
        # Altrimenti tratta l’input come URL YouTube
        audio_path = self.download_audio(source)
        if audio_path.startswith("[❌"):
            return audio_path
        
        return self.transcribe_audio(audio_path)


def extract_insights_from_video(source: str) -> str:
    """Convenience wrapper to use VideoLearner in functional style."""
    learner = VideoLearner()
    return learner.extract_insights_from_video(source)

# Fine modulo — Mercurius∞ è pronto a divorare video, audio e URL senza pietà.
