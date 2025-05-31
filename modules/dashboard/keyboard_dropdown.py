import streamlit as st

def keyboard_input():
    st.markdown('<div class="hud-panel">⌨️ Inserimento manuale olografico</div>', unsafe_allow_html=True)

    preset_options = [
        "Avvia sequenza",
        "Attiva modalità autonoma",
        "Analizza input visivo",
        "Stato del sistema",
        "Salva log"
    ]

    selected = st.selectbox("💬 Comando predefinito:", preset_options)
    custom_input = st.text_input("✍️ Oppure digita qui:", "")

    return custom_input if custom_input.strip() else selected
