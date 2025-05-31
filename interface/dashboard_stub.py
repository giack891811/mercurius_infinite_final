# interface/dashboard.py

"""
Mercurius∞ – Interfaccia Dashboard Unificata (CLI + Streamlit)
Autore: Mercurius Dev AI
Funzioni:
- KPI dinamici (CLI & GUI)
- Drag-and-drop file multimediali
- URL input (YouTube, PDF, Immagini, Web)
- OCR, Parser, Video Analyzer
"""

import streamlit as st
import tempfile
import os
from learning.video_learner import extract_insights_from_video
from learning.document_parser import parse_document
from vision.ocr_module import extract_text_from_image

# ─── Configurazione Base ───────────────────────────────────────────────────────
st.set_page_config(page_title="Mercurius∞ Dashboard", layout="wide")
st.title("🧠 Mercurius∞ Dashboard – Centro di Controllo")

if "kpi" not in st.session_state:
    st.session_state["kpi"] = {}
if "result" not in st.session_state:
    st.session_state["result"] = ""

# ─── KPI View ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📊 KPI & Stato")
    for k, v in st.session_state["kpi"].items():
        st.text(f"{k}: {v}")

# ─── Tab ───────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🌐 Input Multicanale", "📖 Output / Risultati"])

# ─── Tab 1: Input ──────────────────────────────────────────────────────────────
with tab1:
    st.subheader("🔗 Inserisci un URL (YouTube, pagina, documento)")
    url = st.text_input("📎 URL:")
    if url:
        st.info("📺 Estrazione in corso da URL...")
        try:
            output = extract_insights_from_video(url)
            st.session_state["result"] = output
            st.session_state["kpi"]["URL Status"] = "✅ Elaborato"
        except Exception as e:
            st.session_state["result"] = f"Errore: {e}"
            st.session_state["kpi"]["URL Status"] = "❌ Errore"

    st.subheader("📁 Trascina un file (PDF, Immagine, Video)")
    uploaded_file = st.file_uploader("Drag & Drop / Seleziona file", type=["pdf", "jpg", "jpeg", "png", "mp4", "mov"])

    if uploaded_file is not None:
        suffix = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            filepath = tmp.name

        st.success(f"📂 File ricevuto: {uploaded_file.name}")
        result = None

        try:
            if suffix == ".pdf":
                st.info("📑 Analisi PDF...")
                result = parse_document(filepath)
            elif suffix in [".jpg", ".jpeg", ".png"]:
                st.info("🖼️ OCR Immagine...")
                result = extract_text_from_image(filepath)
            elif suffix in [".mp4", ".mov"]:
                st.warning("🎞️ Supporto video locale in sviluppo. Usa un URL YouTube.")
            else:
                st.error("⚠️ Tipo di file non supportato.")

            if result:
                st.session_state["result"] = result
                st.session_state["kpi"]["File Status"] = "✅ Elaborato"
        except Exception as e:
            st.session_state["result"] = f"Errore: {e}"
            st.session_state["kpi"]["File Status"] = "❌ Errore"

# ─── Tab 2: Output ─────────────────────────────────────────────────────────────
with tab2:
    st.subheader("📖 Risultati Apprendimento")
    st.code(st.session_state.get("result", "⏳ Nessun contenuto ancora elaborato."), language="markdown")

# ─── Stub CLI (Fallback o uso parallelo) ───────────────────────────────────────
class DashboardStub:
    def __init__(self):
        self.kpi = {}

    def update(self, name, value):
        self.kpi[name] = value

    def show(self):
        print("=== MERCURIUS∞ CLI DASHBOARD ===")
        for k, v in self.kpi.items():
            print(f"{k:<15}: {v}")
