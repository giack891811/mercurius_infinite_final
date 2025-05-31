# core/emotion_analyzer.py

"""
Modulo: emotion_analyzer.py
Descrizione: Analisi del tono e dell'emozione nel testo tramite NLP per Mercurius∞.
Utilizza VADER per il tono e un classificatore semplice per emozioni.
"""

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import re

# Assicurati che VADER sia disponibile
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


class EmotionAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_tone(self, text: str) -> str:
        """
        Restituisce 'positivo', 'negativo', o 'neutro' in base al tono.
        """
        scores = self.analyzer.polarity_scores(text)
        compound = scores["compound"]
        if compound > 0.2:
            return "positivo"
        elif compound < -0.2:
            return "negativo"
        else:
            return "neutro"

    def detect_emotion(self, text: str) -> str:
        """
        Analisi basilare per mappare parole a emozioni.
        """
        text = text.lower()
        emotion_map = {
            "felice": "gioia",
            "triste": "tristezza",
            "arrabbiato": "rabbia",
            "contento": "gioia",
            "paura": "paura",
            "sorpreso": "sorpresa",
            "odio": "rabbia",
            "ansia": "ansia"
        }

        for keyword, emotion in emotion_map.items():
            if re.search(rf"\b{keyword}\b", text):
                return emotion
        return "neutro"
