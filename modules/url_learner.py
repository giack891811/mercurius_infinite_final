# modules/knowledge/url_learner.py
"""
Scarica pagine web, le riassume con GPT e salva in Long-Term Memory.
"""

import requests, os, openai, readability
from bs4 import BeautifulSoup
from memory.long_term_memory import LongTermMemory
from datetime import datetime
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")
mem = LongTermMemory()                           # usa backend JSON

def _clean_html(html: str) -> str:
    # readability-lxml per estrarre solo il main <article>
    doc = readability.Document(html)
    soup = BeautifulSoup(doc.summary(), "html.parser")
    return soup.get_text(separator="\n")

def summarize(text: str, url: str) -> str:
    prompt = (
        f"Riassumi in 10 bullet il seguente articolo ({url}). "
        "Evidenzia i concetti chiave e gli eventuali numeri importanti.\n\n"
        f"{text[:8000]}"    # taglio altrimenti supero token
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}],
        temperature=0.4, max_tokens=500
    )
    return resp["choices"][0]["message"]["content"]

def ingest_url(url: str):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    text = _clean_html(r.text)
    summary = summarize(text, url)
    mem.save_experience({
        "tags": ["url_knowledge"],
        "source": url,
        "summary": summary
    })
    print(f"✅ Ingested {url}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m modules.knowledge.url_learner <url1> <url2> …")
        raise SystemExit
    for u in sys.argv[1:]:
        ingest_url(u)
