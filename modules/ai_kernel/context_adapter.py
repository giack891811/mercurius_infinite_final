"""
Modulo: context_adapter
Descrizione: Adatta il contesto conversazionale e ambientale per l'agente Mercurius∞.
Autore: Mercurius∞ AI Engineer
"""

class ContextAdapter:
    def __init__(self):
        self.current_context = {
            "user": "Germano",
            "mode": "interactive",
            "location": "desktop",
            "language": "it",
            "time": "giorno"
        }

    def update_context(self, key: str, value):
        self.current_context[key] = value

    def get_context(self):
        return self.current_context

    def summarize_context(self):
        parts = [f"{k}: {v}" for k, v in self.current_context.items()]
        return " | ".join(parts)

# Test rapido
if __name__ == "__main__":
    ca = ContextAdapter()
    ca.update_context("location", "Note 10+")
    print("Contesto attuale:", ca.summarize_context())
