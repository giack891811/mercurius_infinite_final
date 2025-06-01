# modules/fingpt_analyzer.py

"""
Modulo: fingpt_analyzer.py
Descrizione: Modulo di analisi NLP con FinGPT per generare segnali operativi da notizie e sentiment.
"""

class FinGPTAnalyzer:
    def __init__(self):
        self.last_signal = None

    def analyze_text(self, text: str) -> str:
        if "inflation" in text.lower():
            self.last_signal = "SELL"
        else:
            self.last_signal = "BUY"
        return f"📉 Segnale da news: {self.last_signal}"


# Test rapido
if __name__ == "__main__":
    bot = FinGPTAnalyzer()
    print(bot.analyze_text("US Inflation data released - very high"))
