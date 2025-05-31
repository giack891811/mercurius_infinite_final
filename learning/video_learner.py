# learning/video_learner.py

"""
Modulo: video_learner.py
Descrizione: Apprendimento da contenuti video. Estrae audio, converte in testo via STT,
e genera sintesi concettuale.
"""

from pytube import YouTube
import os
import tempfile
import moviepy.editor as mp
import speech_recognition as sr


class VideoLearner:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def download_audio(self, url: str) -> str:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_path = os.path.join(tempfile.gettempdir(), "yt_audio.mp4")
        audio_stream.download(output_path=output_path, filename="yt_audio.mp4")
        return output_path

    def convert_to_wav(self, mp4_path: str) -> str:
        wav_path = mp4_path.replace(".mp4", ".wav")
        try:
            clip = mp.AudioFileClip(mp4_path)
            clip.write_audiofile(wav_path, logger=None)
        except Exception as e:
            return f"[Errore conversione WAV]: {e}"
        return wav_path

    def transcribe_audio(self, wav_path: str) -> str:
        with sr.AudioFile(wav_path) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_google(audio, language="it-IT")
        except sr.UnknownValueError:
            return "[Audio non riconosciuto]"
        except sr.RequestError:
            return "[Errore richiesta STT]"

    def extract_insights_from_video(self, url: str) -> str:
        """
        Processo completo: download → conversione → trascrizione.
        """
        mp4_path = self.download_audio(url)
        wav_path = self.convert_to_wav(mp4_path)
        transcript = self.transcribe_audio(wav_path)
        return transcript
