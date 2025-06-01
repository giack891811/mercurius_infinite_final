# monitoring/log_dashboard.py

"""
Modulo: log_dashboard.py
Descrizione: Dashboard Streamlit per visualizzare in tempo reale l’Audit Log di Mercurius∞.
Espone una tabella che mostra le ultime righe di “logs/audit_log.jsonl” e si aggiorna ogni 2 secondi.
"""

import json
from pathlib import Path

import streamlit as st

# Percorso del file di log in formato JSON Lines
LOG_FILE = Path("logs/audit_log.jsonl")

# Configurazione della pagina Streamlit
st.set_page_config(layout="wide", page_title="Mercurius∞ – Audit Log Live")
st.title("🛡️ Mercurius∞ – Live Audit Log")

# Placeholder che verrà rimpiazzato con la tabella dei log
placeholder = st.empty()


def tail_log(n: int = 200):
    """
    Legge le ultime `n` righe del file di log (se presente) e le restituisce
    come lista di dizionari JSON. Se il file non esiste, ritorna lista vuota.

    :param n: numero di righe finali da leggere (default 200)
    :return: lista di oggetti (dict) corrispondenti alle righe JSON più recenti
    """
    if not LOG_FILE.exists():
        return []
    # Legge tutto il testo del file, lo divide per righe e ne restituisce le ultime n
    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()[-n:]
    return [json.loads(line) for line in lines]


# Loop infinito: ogni 2 secondi aggiorna la tabella con gli ultimi log
while True:
    data = tail_log()
    placeholder.table(data)
    st.sleep(2)
