"""
Modulo: huggingface_tools.py
Responsabilità: Integrazione task avanzati HuggingFace (NLP, NLU, visione, ecc.)
Autore: Mercurius∞ AI Engineer
"""

class HuggingFaceTools:
    def __init__(self):
        try:
            from transformers import pipeline
            self.pipeline = pipeline
            self.ready = True
        except ImportError:
            self.pipeline = None
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def run_task(self, task: str, input_data: str) -> str:
        """
        Esegue un task NLP/NLU HuggingFace (es. sentiment-analysis, summarization, ecc.).
        """
        if not self.ready:
            return "[❌ HuggingFace non disponibile]"
        try:
            pipe = self.pipeline(task)
            result = pipe(input_data)
            return str(result)
        except Exception as e:
            return f"[❌ Errore HuggingFace]: {e}"
