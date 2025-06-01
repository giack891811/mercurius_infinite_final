# modules/feedback_loop.py

"""
Modulo: feedback_loop.py
Descrizione: Coordina il feedback tra moduli AI in Mercurius∞ per auto-apprendimento, miglioramento codice e decisioni collettive.
"""

class FeedbackLoop:
    def __init__(self):
        self.logs = []

    def collect_feedback(self, source: str, message: str):
        entry = f"🔁 [{source}] → {message}"
        self.logs.append(entry)
        print(entry)

    def last_feedback(self, n=5):
        return "\n".join(self.logs[-n:])


# Test rapido
if __name__ == "__main__":
    fb = FeedbackLoop()
    fb.collect_feedback("AZR", "Codice semanticamente corretto.")
    fb.collect_feedback("GPT-4o", "Suggerita ottimizzazione per compatibilità.")
    print(fb.last_feedback())
