# AION – Advanced Intelligence Of Nexus

🔬 **AION** è un sistema AI evolutivo full-stack, autonomo, multimodale e cognitivamente attivo.
Progettato per **apprendere**, **riflettere**, **generare codice** e **interagire** con ambienti complessi in tempo reale.

## 🧠 Caratteristiche Principali

- 🧠 **Autonomia cognitiva** – Apprende da esperienze passate, simula riflessioni e ottimizza strategie.
- 🗺️ **Pianificazione intelligente** – Crea piani operativi e migliora tramite feedback (AZR).
- 🎤 **Multimodalità attiva** – Supporta voce, testo, immagini e input sensoriali reali.
- 🛠️ **Autogenerazione codice** – Scrive e modifica moduli Python in autonomia.
- 📊 **Supervisione interna** – Telemetria cognitiva, metriche performance e logging avanzato.
- 🧩 **Architettura modulare** – Ogni componente è plug&play e indipendente.

---

## 📂 Struttura del Progetto

```plaintext
├── main.py                    # Entry point principale
├── start_fullmode.py         # Avvio completo in modalità "Jarvis+"
├── modules/
│   ├── Neo/                  # Agenti evolutivi, ragionamento e simulazione
│   ├── GPT/                  # Prompting e generazione LLM
│   ├── AZR/                  # Modulo Reasoning e feedback
│   ├── dashboard/            # Interfaccia utente (Tk + Streamlit)
│   └── Reasoner/             # Catene logiche e planning
├── tools/                    # Logger, loader, scheduler, tester
├── config/                   # Configurazioni e ambienti
├── culture/                  # File cognitivi e conoscenza appresa
└── memory/                   # Memoria esperienziale degli agenti

## 🚀 Modalità GENESIS
Per avviare Mercurius∞ con tutti i moduli attivi, eseguire:

```bash
python scripts/aion_boot.py
```

Il comando abilita la rete di agenti (OpenAI, Ollama, AZR), la voce (Whisper + gTTS) e la visione YOLO tramite webcam IP.

## 🛰 Mission Controller Evolutivo
Il file `orchestrator/mission_controller.py` introduce un controller che gestisce un ciclo di self-questioning tra gli agenti (Reasoner, AZR e Codex). Ogni workspace contiene un prompt dedicato e il controller salva log e patch generate in automatico.

Per una prova rapida è disponibile la GUI Streamlit:

```bash
streamlit run modules/dashboard/mission_gui.py
```

Da qui è possibile creare nuovi workspace, avviare il ciclo evolutivo e visualizzare i log della sandbox.

## 🛠 Generazione automatica del prompt per GPT-Engineer

Sono disponibili tre script per creare i file di lavoro:

1. `scripts/update_project_tree.py` aggiorna `project_tree.txt` con l'albero del repository e le prime 100 righe dei file di testo.
2. `scripts/build_prompt.py` unisce `project_tree.txt` e `prompt_commands.txt` nel file finale `prompt.txt`.
3. `update_project_tree.py` salva in `project_tree` tutti i file testuali del progetto con percorso e contenuto completo.
4. `split_project_tree.py` divide `project_tree` in chunk sequenziali `project_tree_partN.txt` da massimo 17.000 righe.

### Utilizzo manuale

```bash
python scripts/update_project_tree.py
python scripts/build_prompt.py
python update_project_tree.py
python split_project_tree.py
./update_tree_parts.sh  # esegue gli ultimi due comandi con un solo passo
```

### Integrazione con Git

```bash
# abilita i githook personalizzati
git config core.hooksPath githooks
```

`githooks/post-merge` aggiorna `project_tree.txt` e ricrea `project_tree` con i relativi file `project_tree_partN.txt` dopo ogni merge.
`githooks/pre-commit` genera `project_tree`, lo suddivide nei file `project_tree_partN.txt` e li aggiunge al commit.
Attiva l'hook con:
`git config core.hooksPath githooks && chmod +x githooks/pre-commit`
(valido sia su Linux che su Windows con Git Bash).

