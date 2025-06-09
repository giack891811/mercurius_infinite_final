def run_codex_from_md(path: str) -> str:
    """
    Legge un file markdown contenente un prompt e lo passa a Codex per l'esecuzione automatica.
    Il path è relativo alla root del progetto.

    :param path: Percorso del file markdown contenente la missione
    :return: Output generato da Codex o messaggio di errore
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            mission_prompt = f.read()

        # Simulazione chiamata a Codex – sostituisci con Codex reale se integrato
        print(f"🔧 Eseguo missione Codex da: {path}")
        return f"[OK] Missione Codex eseguita da '{path}'"
        
    except Exception as e:
        return f"[ERRORE] Impossibile eseguire Codex da '{path}': {str(e)}"

