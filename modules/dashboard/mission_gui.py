"""mission_gui.py
GUI minimale per interagire con il Mission Controller.
"""

import streamlit as st
from orchestrator.mission_controller import MissionController
from modules.strategic.strategic_brain import StrategicBrain

st.set_page_config(page_title="Mission Control")

if "controller" not in st.session_state:
    st.session_state.controller = MissionController()
if "strategic" not in st.session_state:
    st.session_state.strategic = StrategicBrain()

mc = st.session_state.controller
sb = st.session_state.strategic

st.title("🚀 Mercurius∞ Mission Control")

with st.form("new_workspace"):
    name = st.text_input("Nome workspace", "workspace1")
    prompt = st.text_area("Prompt o progetto")
    submitted = st.form_submit_button("Crea workspace")
    if submitted:
        mc.create_workspace(name, prompt)
        st.success(f"Workspace '{name}' creato")

st.markdown("## 🧠 Strategic Brain")
if st.button("Carica goals.txt"):
    sb.load_goals("goals.txt")
    st.success("Goals caricati")
if sb.goal_manager.pending_goals():
    if st.button("Esegui Strategic Brain"):
        outputs = sb.run()
        for out in outputs:
            st.text(out)

selected = st.selectbox("Scegli workspace", list(mc.workspaces.keys())) if mc.workspaces else None
if selected:
    if st.button("Esegui ciclo evolutivo"):
        mc.run_cycle(selected)
        st.success("Ciclo completato")
    if st.checkbox("Mostra log" ):
        log_path = mc.workspaces[selected]["path"] / "sandbox.log"
        if log_path.exists():
            st.text(log_path.read_text())

