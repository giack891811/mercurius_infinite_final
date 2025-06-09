def run_codex_from_md(path: str) -> str:
    """
    Esegue un prompt Codex a partire da un file .md contenente una missione SELF_MISSION.

    :param path: Percorso del file Markdown contenente la missione
    :return: Risultato (stdout simulato o reale)
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            mission_prompt = f.read()

        # 🔁 Simula esecuzione prompt
        print(f"⚙️  Eseguo SELF_MISSION da file: {path}")
        print(f"📝 Prompt letto:\n{mission_prompt[:300]}...")

        # Qui potrai integrare il vero motore Codex
        return f"✅ Prompt eseguito con successo da '{path}'"

    except Exception as e:
        return f"❌ Errore durante lettura o esecuzione del file '{path}': {e}"
