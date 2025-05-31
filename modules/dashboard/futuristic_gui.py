import streamlit as st
from modules.voice_bridge.tts_engine import Pyttsx3TTS
from modules.ai_kernel.agent_core import AgentCore
from modules.dashboard.keyboard_dropdown import keyboard_input
import base64

# ────────────────────────────────────────────────────────────────────────────────
# 🧬 STILE HOLOGRAFICO PERSONALIZZATO
def load_custom_css():
    with open("modules/dashboard/hud.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# 🧠 COMPONENTI INIZIALI
agent = AgentCore()
tts = Pyttsx3TTS()

# ────────────────────────────────────────────────────────────────────────────────
# 🚀 STREAMLIT GUI
st.set_page_config(layout="wide", page_title="Mercurius∞ HUD")
load_custom_css()

st.markdown('<div class="hud-header">MERCURIUS∞ // INTERFACCIA OLOGRAFICA</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="hud-panel">🧠 STATO AGENTE</div>', unsafe_allow_html=True)
    st.write(f"Nome: {agent.name}")
    st.write(f"Stato: {agent.status}")
    st.markdown("---")
    text_input = keyboard_input()

    if st.button("🗣️ Rispondi"):
        agent.perceive(text_input)
        decision = agent.reason()
        agent.act(decision)
        tts.speak(decision)
        st.success(f"Risposta: {decision}")

with col2:
    st.markdown('<div class="hud-panel">📊 LOG</div>', unsafe_allow_html=True)
    st.text_area("Memoria", value="\n".join(agent.memory), height=300)

st.markdown('<div class="hud-footer">🛰 Mercurius∞ 2025 – Modalità Olografica Attiva</div>', unsafe_allow_html=True)
