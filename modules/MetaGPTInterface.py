"""Interfaccia minima per MetaGPT."""

class MetaGPTInterface:
    def ask(self, prompt: str) -> str:
        """Restituisce una risposta simulata."""
        return f"[MetaGPT] {prompt}"

    def generate_code(self, requirement: str) -> str:
        """Genera codice di esempio a partire da una descrizione."""
        return f"# codice generato per: {requirement}\nprint('todo')"
