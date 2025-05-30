import streamlit as st
from modules.Neo.self_awareness import get_current_state
from modules.Neo.context_memory import get_recent_context
from modules.Neo.interaction_style import get_style

st.set_page_config(page_title="Mercurius∞ Dashboard", layout="wide")

st.title("🧠 Mercurius∞ – Interfaccia Cognitiva")

col1, col2 = st.columns(2)

with col1:
    st.header("🧬 Stato interno")
    state = get_current_state()
    st.json(state)

    st.header("🎙️ Stile comunicativo")
    st.write(get_style())

with col2:
    st.header("🔁 Contesto recente")
    st.write(get_recent_context())

st.markdown("---")
st.success("Dashboard aggiornata e funzionante.")