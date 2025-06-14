#PROMPT_TYPE: Deep Audit  
#ROLE: AI System Auditor + Finetuning Inspector  
#MODEL: gpt-4o  
#GOAL: Rapporto OGGETTIVO e AGGIORNATO di **tutto** Mercurius∞  
#PERMISSION: Lettura + scrittura permanente via API JOSCH  

---

```python run
"""
Questo blocco gira *dentro* run_selfmission.py (stesso venv di Mercurius∞).
Fa chiamate HTTP a JOSCH per leggere i file e produce il report.
"""

import json, re, textwrap, datetime as dt, requests, pathlib, ast, importlib.util, collections, os, sys

BASE_URL = "http://localhost:3020"
BASE = pathlib.Path(__file__).resolve().parent.parent  # root progetto

# ───────────────────── Helper ─────────────────────
def api(path: str, **params):
    """Chiamata GET con timeout e gestione errori."""
    r = requests.get(BASE_URL + path, params=params, timeout=5)
    r.raise_for_status()
    return r.json()

def today() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")

def analyse(src: str):
    """Ritorna (icona, stato, flag_finetune)."""
    if not src.strip():
        return "❌", "Vuoto", False
    todo = bool(re.search(r"\bTODO\b|pass\b|NotImplemented", src))
    finetune = bool(re.search(r"\.(ckpt|pt)\b|Trainer|wandb", src, re.I))
    try:
        ast.parse(src)
        icon = "⚠" if todo else "✅"
    except SyntaxError:
        icon, todo = "❌", True
    msg = "Finetuning" if finetune else ("Parziale" if todo else "OK")
    return icon, msg, finetune

# ───────────────────── Start ─────────────────────
# sanity-check server
assert api("/ping") == {"pong": "ok"}, "JOSCH non risponde su /ping"

files = api("/list_files")
batch_size = 15
batches = [files[i : i + batch_size] for i in range(0, len(files), batch_size)]

summary = collections.Counter()
missing, dups = set(), []
report = [
    "# 📘 Full Project Audit – Mercurius∞",
    "",
    f"_Generated: {today()}_",
    "",
]

for bi, blk in enumerate(batches, 1):
    report.append(f"## 🔍 Batch {bi}")
    for fp in blk:
        src = api("/read_file", filepath=fp)["content"]
        icon, msg, ft = analyse(src)
        report.append(f"- {icon} `{fp}` — {msg}")
        summary[icon] += 1
        # importa mancanti
        for m in re.findall(r"^(?:from|import)\s+([\w\.]+)", src, re.M):
            root = m.split(".")[0]
            if importlib.util.find_spec(root) is None and root not in files:
                missing.add(root)
    report.append("")

# duplicati tra src/ e temp_clean/
for f in files:
    cleaned = f.replace("temp_clean/", "").replace("src/", "")
    if cleaned != f and cleaned in files:
        dups.append(f)

# executive summary
ok, warn, bad = summary["✅"], summary["⚠"], summary["❌"]
finetune_tot = sum(
    analyse(api("/read_file", filepath=f)["content"])[2] for f in files
)
report.insert(3, f"**Totale file:** {len(files)} | ✅ {ok} ⚠ {warn} ❌ {bad}")
report.insert(4, f"**Moduli finetuning:** {finetune_tot}")

report.append("## 🧩 Import mancanti")
report.extend(f"- {m}" for m in sorted(missing) or ["Nessuno"])

report.append("\n## 🗄️ Duplicati src/ vs temp_clean/")
report.extend(f"- {d}" for d in dups or ["Nessuno"])

report.append("\n## 💡 Raccomandazioni")
report += [
    "- Scrivere test per tutti i moduli ⚠ / ❌",
    "- Unificare i duplicati (scegliere una sola copia)",
    "- Verificare i moduli di finetuning segnalati",
]

# salva report definitivo
rep_path = f"logs/full_project_audit_{today()}.md"
(BASE / rep_path).parent.mkdir(parents=True, exist_ok=True)
(BASE / rep_path).write_text("\n".join(report), encoding="utf-8")
print(f"[OK] Audit scritto in {rep_path}")
```                     

write_file("logs/full_project_audit_placeholder.md", <<EOF)
# Audit placeholder
(Questo file prova che **write_file** viene eseguito.)
EOF
