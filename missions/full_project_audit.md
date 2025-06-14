#PROMPT_TYPE: Full Codebase Audit
#ROLE: AI Codebase Reviewer
#GOAL: Analizza tutto il codice del progetto `mercurius_infinite_final` via JOSCH.

## Obiettivi principali

1. Identificare moduli funzionanti.
2. Segnalare moduli incompleti o orfani.
3. Verificare comunicazione corretta tra i file Python.
4. Controllare la presenza di funzionalità AI: visione, reasoning, trading, finetuning, auto-evoluzione.
5. Restituire un **report Markdown** strutturato.

## Regole

- Usa solo le API Josh:
  - `/list_files`
  - `/read_file`
  - `/write_file`
- Analizza tutti i `.py` nei percorsi:
  - `orchestrator/`, `modules/`, `scripts/`, `codex/`, `agents/`, `integrations/`
- Non allucinare: se un modulo non è connesso, **dillo** chiaramente.
- Se trovi errori nei `from ... import ...`, segnala e suggerisci fix.

## Output atteso

```markdown
### ✅ Moduli Attivi
- `core/self_tuner.py`: attivo e connesso al Reasoner
- `modules/llm/azr_reasoner.py`: attivo e validato

### ❌ Moduli Incompleti / Orfani
- `memory/synaptic_log.py`: definito ma non richiamato da nessun orchestratore
- `network_analyzer.py`: presenta import errato (`bluetooth` obsoleto)

### 🔗 Comunicazione tra Moduli
- 85% dei moduli sono collegati tramite `genesis_orchestrator.py`
- Alcuni file sono duplicati nella cartella `temp_clean/` – pulire.

### 🧠 Funzionalità AI rilevate
- Visione artificiale: ✅ (`eye_agent.py`)
- Reasoning multi-LLM: ✅
- Auto-evoluzione via `SELF_MISSION`: ✅
- Finetuning: 🔸 (presente ma non connesso)
- Trading: ⚠️ `MetaTrader5` non disponibile

