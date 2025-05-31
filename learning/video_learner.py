# learning/video_learner.py

"""
Modulo: video_learner.py
Descrizione: Apprendimento da contenuti video (es. YouTube). 
Estrae audio → converte in testo via STT → restituisce sintesi concettuale.
Supporta fallback se i moduli non sono disponibili.
"""

import os
import tempfile

# ─── Import Condizionali ─────────────────────────────────────────────────────
try:
    from pytube import YouTube
    import moviepy.editor as mp
    import speech_recognition as sr
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False


class VideoLearner:
    def __init__(self):
        if MODULES_AVAILABLE:
            self.recognizer = sr.Recognizer()
        else:
            self.recognizer = None

    def download_audio(self, url: str) -> str:
        """
        Scarica solo l'audio da un video YouTube in formato MP4.
        """
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_path = os.path.join(tempfile.gettempdir(), "yt_audio.mp4")
        audio_stream.download(output_path=output_path, filename="yt_audio.mp4")
        return output_path

    def convert_to_wav(self, mp4_path: str) -> str:
        """
        Converte il file MP4 audio in WAV per la trascrizione.
        """
        wav_path = mp4_path.replace(".mp4", ".wav")
        try:
            clip = mp.AudioFileClip(mp4_path)
            clip.write_audiofile(wav_path, logger=None)
        except Exception as e:
            return f"[Errore conversione WAV]: {e}"
        return wav_path

    def transcribe_audio(self, wav_path: str) -> str:
        """
        Converte l'audio WAV in testo usando Google Speech Recognition.
        """
        try:
            with sr.AudioFile(wav_path) as source:
                audio = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio, language="it-IT")
        except sr.UnknownValueError:
            return "[⚠️ Audio non riconosciuto]"
        except sr.RequestError:
            return "[❌ Errore servizio di trascrizione]"

    def extract_insights_from_video(self, url: str) -> str:
        """
        Processo completo: download → conversione → trascrizione.
        """
        if not MODULES_AVAILABLE:
            return "[❌ Moduli STT mancanti: pytube, moviepy, speech_recognition]"

        try:
            mp4_path = self.download_audio(url)
            wav_path = self.convert_to_wav(mp4_path)
            if "Errore" in wav_path:
                return wav_path
            transcript = self.transcribe_audio(wav_path)
            return transcript
        except Exception as e:
            return f"[❌ Errore STT video]: {e}"
