# memory/memory_core.py

"""
Modulo: memory_core.py
Descrizione: Gestione unificata della memoria cognitiva (a lungo termine, episodica e log sinaptico)
per Mercurius∞. Punto centrale di accesso e coordinamento dei moduli mnemonici.
"""

from memory.long_term_memory import LongTermMemory
from memory.episodic_memory import EpisodicMemory
from memory.synaptic_log import SynapticLog


class MemoryCore:
    def __init__(self):
        self.long_term = LongTermMemory()
        self.episodic = EpisodicMemory()
        self.synaptic_log = SynapticLog()
        self.synaptic_log.log_event("MemoryCore", "initialized")

    def store_fact(self, content: str, category: str = "general"):
        self.long_term.store_memory(content, category)
        self.synaptic_log.log_event("LongTermMemory", "store_fact", f"Category: {category}")

    def recall_facts(self, category: str = None, limit: int = 10):
        facts = self.long_term.retrieve_memories(category, limit)
        self.synaptic_log.log_event("LongTermMemory", "recall_facts", f"Category: {category}")
        return facts

    def record_interaction(self, context: str, user_input: str, ai_response: str):
        self.episodic.record_episode(context, user_input, ai_response)
        self.synaptic_log.log_event("EpisodicMemory", "record_interaction", f"Input: {user_input[:30]}...")

    def review_recent_episodes(self, limit: int = 5):
        episodes = self.episodic.get_recent_episodes(limit)
        self.synaptic_log.log_event("EpisodicMemory", "review_recent_episodes")
        return episodes

    def search_knowledge(self, keyword: str):
        facts = self.long_term.search_memory(keyword)
        episodes = self.episodic.search_episodes(keyword)
        self.synaptic_log.log_event("MemoryCore", "search_knowledge", f"Keyword: {keyword}")
        return {"facts": facts, "episodes": episodes}
