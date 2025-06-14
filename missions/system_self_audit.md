#PROMPT_TYPE: System Self-Audit  
#ROLE: AI Codebase Inspector + System Diagnostician  
#TARGET_PROJECT: mercurius_infinite_final/  
#GOAL: Analizzare sinceramente e oggettivamente lo stato reale del sistema Mercurius∞, verificando se tutto funziona come previsto.

---

## 🎯 Obiettivo

Esegui una scansione **lenta e approfondita (30 minuti)** per valutare:

1. Quali moduli sono realmente **funzionanti**
2. Quali sono solo **parzialmente implementati** o **non collegati**
3. Se i file **comunicano correttamente tra loro**
4. Se esistono funzionalità di:
   - ✅ **Fine-tuning**
   - ✅ **Reasoning**
   - ✅ **Visione artificiale**
   - ✅ **Elaborazione vocale**
   - ✅ **Trading**
   - ✅ **Auto-evoluzione**

---

## 📜 Regole operative

- Continua a lavorare **finché non hai completato la missione**
- Se non conosci un modulo, **apri il file**, leggi e deduci il funzionamento
- **Non allucinare**: sii oggettivo, sincero e tecnico
- Pianifica attentamente ogni passaggio e **ragiona sempre sui risultati**
- Controlla:
  - ✅ Import
  - ✅ Dipendenze
  - ✅ Comunicazione da `genesis_orchestrator.py`
  - ✅ Attivazione da `SELF_MISSION` o moduli esterni

---

## 📂 Percorsi chiave da scandagliare

- `orchestrator/`
- `modules/llm/`, `scheduler/`, `vision/`, `memory/`, `codex/`
- `integrations/`, `agents/`, `scripts/`, `tests/`
- `missions/` (`prompt_di_dio.md`, `repair_missing_modules.md`)

---

## 📦 Output richiesto (in Markdown)

Restituisci un report con:

### ✅ Moduli Attivi
Elenco dei moduli realmente funzionanti, con spiegazione delle loro funzionalità reali.

### ❌ File Orfani
File presenti ma non importati, non richiamati o mai utilizzati.

### 🔁 Comunicazione tra Moduli
Verifica se esistono connessioni reali (import, chiamate, pipeline) tra i moduli chiave.

### 🧠 Funzionalità AI Effettive
Specifica quali moduli AI sono presenti e realmente operativi:
- [ ] Visione artificiale
- [ ] Elaborazione vocale
- [ ] Reasoning (con AZR)
- [ ] Fine-tuning attivo
- [ ] Trading (con `trading_core.py`)
- [ ] Self evolution / tuning

### 🧬 Livello di Auto-Evoluzione
Valuta quanto il sistema è **autonomo** nel correggersi, adattarsi e migliorarsi da solo.  
Dai un giudizio oggettivo (es: "40% completato").

---

## 🚨 Obbligatorio

- Includi **nomi file**, **percorso**, e stato per ogni modulo  
- Se rilevi errori o disconnessioni, **suggerisci come sistemarli**  
- Valida il report con AZR se attivo  
- Salva un log automatico in `logs/system_self_audit.md`
