#PROMPT_TYPE: Deep Audit  
#ROLE: AI System Auditor + Finetuning Inspector  
#MODEL: gpt-4o  
#GOAL: Rapporto **oggettivo e aggiornato** sull’intero codice Mercurius∞  
#PERMISSION: Lettura + scrittura permanente via API JOSCH  

---

```python run
"""
Full Project Deep-Audit – Mercurius∞
Genera un report Markdown completo e lo salva in logs/.
© 2025
"""
import re, ast, datetime, importlib.util, requests, textwrap, pathlib, collections
from run_selfmission import _save_block   # funzione helper già disponibile

API   = "http://localhost:3020"
BASE  = pathlib.Path(__file__).resolve().parent.parent
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

def api(path):
    return requests.get(f"{API}{path}")

def analyse(src:str):
    if not src.strip():
        return "❌", "Vuoto"
    finetune = bool(re.search(r'\.(ckpt|pt)\b|Trainer\b|wandb', src, re.I))
    try:
        ast.parse(src)
        todo = bool(re.search(r'\bTODO\b|pass\b|NotImplemented', src))
        icon  = "⚠" if todo else "✅"
        label = "Parziale" if todo else "OK"
    except SyntaxError:
        icon, label = "❌", "Syntax error"
    if finetune:
        label += " | Finetuning"
    return icon, label

files  = api("/list_files").json()
batch  = 15
batches= [files[i:i+batch] for i in range(0, len(files), batch)]

report = [f"# 📘 Full Project Audit – Mercurius∞",
          f"_Generated: {TODAY}_", ""]

import_missing = set()
dupes          = []

for idx, group in enumerate(batches, 1):
    report.append(f"## 🔍 Batch {idx}")
    for f in group:
        src = api(f"/read_file?filepath={f}").json()["content"]
        icon, label = analyse(src)
        report.append(f"- {icon} `{f}` — {label}")
        # import check
        for m in re.findall(r'^(?:from|import) +([\\w\\.]+)', src, re.M):
            root = m.split('.')[0]
            try:
                importlib.util.find_spec(root)
            except ModuleNotFoundError:
                import_missing.add(root)
        # duplicate check
        clean = f.replace('temp_clean/', '').replace('src/', '')
        if clean != f and clean in files:
            dupes.append(f)
    report.append("")

# executive summary
count = collections.Counter(re.match(r'- (.)', line).group(1) for line in report if line.startswith('- '))
total = len(files)
report.insert(2, f"**Totale file:** {total}  |  ✅ {count['✅']}  ⚠ {count['⚠']}  ❌ {count['❌']}")

# sezioni extra
report.append("## 🧩 Dipendenze mancanti")
report.extend(f"- {m}" for m in sorted(import_missing) or ["Nessuna"])

report.append("\n## 🗄️ Moduli duplicati")
report.extend(f"- {d}" for d in dupes or ["Nessuno"])

report.append("\n## 💡 Raccomandazioni")
report.append("- Aggiungere test per i file ⚠ / ❌")
report.append("- Consolidare duplicati di `src/` e `temp_clean/`")
report.append("- Controllare i moduli marcati «Finetuning» per eventuale training incompleto")

# scrittura file (due copie: latest + datata)
content = "\n".join(report)
_save_block(f"logs/full_project_audit_latest.md", content)
_save_block(f"logs/full_project_audit_{TODAY}.md", content)
print("[OK] Report generato e salvato")
