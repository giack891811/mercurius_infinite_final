# rag/insight_rag.py

"""
Modulo: insight_rag.py
Descrizione: Sistema di archiviazione e recupero semantico (RAG) per concetti estratti da fonti multimodali.
"""

import os
import json
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

class InsightRAG:
    def __init__(self, db_path="logs/insight_memory.json"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.db_path = db_path
        self.embeddings = []
        self.memory = []
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                self.memory = json.load(f)
                self.embeddings = [item["embedding"] for item in self.memory]

    def save_memory(self):
        with open(self.db_path, "w") as f:
            json.dump(self.memory, f, indent=2)

    def embed_insight(self, content: str):
        embedding = self.model.encode(content).tolist()
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "text": content,
            "embedding": embedding
        }
        self.memory.append(entry)
        self.embeddings.append(embedding)
        self.save_memory()

    def query_concepts(self, question: str, top_k=3) -> list:
        query_emb = self.model.encode(question)
        scores = util.cos_sim(query_emb, self.embeddings)[0]
        top_indices = scores.argsort(descending=True)[:top_k]
        return [self.memory[idx] for idx in top_indices]

    def rank_relevance(self):
        return sorted(self.memory, key=lambda x: x["timestamp"], reverse=True)[:10]
