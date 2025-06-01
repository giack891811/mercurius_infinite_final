# modules/hf_tools_manager.py

"""
Modulo: hf_tools_manager.py
Descrizione: Integrazione con HuggingFace Transformers Agents per interagire con strumenti locali.
"""

from transformers import HfAgent

class HFToolsManager:
    def __init__(self):
        self.agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")

    def use_tool(self, query: str) -> str:
        try:
            return self.agent.run(query)
        except Exception as e:
            return f"❌ Errore HuggingFace Tools: {str(e)}"
