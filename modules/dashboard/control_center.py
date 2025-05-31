"""
Modulo: control_center
Descrizione: Interfaccia Streamlit per controllo agenti Mercurius∞ (stub).
Autore: Mercurius∞ AI Engineer
"""

import streamlit as st

def main():
    st.set_page_config(page_title="Mercurius∞ Control", layout="wide")
    st.title("🚀 Mercurius∞ Control Center")
    st.markdown("Benvenuto nella dashboard operativa.")

    with st.sidebar:
        st.header("Controlli di Sistema")
        st.button("Avvia Agente")
        st.button("Ascolta Audio")
        st.button("Elabora Ragionamento")
    
    st.write("🧠 Stato dell'agente:")
    st.success("Agente attivo e in ascolto.")

if __name__ == "__main__":
    main()
