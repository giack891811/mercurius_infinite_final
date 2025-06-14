"""run_selfmission.py – HYPER v3.3-robust | Mercurius∞"""

from __future__ import annotations
import io, json, os, re, subprocess, sys, textwrap, time, traceback, uuid
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from typing import Any, Dict, List

# ═══════════════════ Config ════════════════════════════════
def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / ".git").exists():
            return p
    return Path.cwd()

BASE_PATH = repo_root()
LOG_FILE  = BASE_PATH / "logs" / "selfmission_last.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

WRITE_RE = re.compile(
    r'write_file\(\s*"(?P<path>[^"]+)"\s*,\s*<<EOF\s*(?P<body>.*?)\s*EOF\)',
    re.I | re.S,
)
CODE_RE = re.compile(
    r"""
    ^\s*```[ \t]*(?P<lang>python|bash|mission)[ \t]+run[ \t]*\r?\n
    (?P<body>.*?)\r?\n\s*```[ \t]*$
    """, re.I | re.S | re.M | re.X,
)

# ═══════════════ Utility ═══════════════════════════════════
def _log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8", errors="replace") as fh:
        fh.write(f"{ts} | {msg}\n")
    print(msg)

def _save_block(rel: str, body: str) -> str:
    path = BASE_PATH / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    body = textwrap.dedent(body).lstrip("\n")
    path.write_text(body, encoding="utf-8")
    _log(f"📝 write_file → {rel} ({len(body.splitlines())} linee)")
    return str(path.relative_to(BASE_PATH))

def _exec_python(code: str) -> str:
    out, err = io.StringIO(), io.StringIO()
    t0 = time.perf_counter()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            exec(code, {"__name__": "__mission__"})
    except Exception:
        traceback.print_exc(file=err)
    dt = time.perf_counter() - t0
    _log(f"⚙️  python {dt:.2f}s • stdout={len(out.getvalue())}B • stderr={len(err.getvalue())}B")
    return out.getvalue() + err.getvalue()

def _exec_bash(cmd: str) -> str:
    if os.name == "nt":
        shell_cmd, shell = ["powershell", "-NoLogo", "-Command", cmd], False
    else:
        shell_cmd, shell = cmd, True
    p = subprocess.run(shell_cmd, shell=shell, capture_output=True, text=True,
                       cwd=BASE_PATH, timeout=30)
    _log(f"⚙️  bash rc={p.returncode} • stdout={len(p.stdout)}B • stderr={len(p.stderr)}B")
    return p.stdout + p.stderr

# ═════════════ Runner ══════════════════════════════════════
def run_md(rel: str, *, depth=0, quiet=False) -> str:
    if depth > 2:
        return "[ABORT] Ricorsione mission troppo profonda"
    md_path = BASE_PATH / rel
    if not md_path.exists():
        return f"[ERRORE] File non trovato: {rel}"

    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:  # encoding or I/O issues
        return f"[ERRORE] Lettura {rel} fallita: {e}"

    matches = list(CODE_RE.finditer(text))
    if not quiet:
        print(f"DEBUG ‣ {rel}  blocchi={len(matches)}", file=sys.stderr)

    if not matches:
        return "[ERRORE] 0 blocchi trovati – controlla il Markdown"

    written, executed = [], []
    for m in WRITE_RE.finditer(text):
        written.append(_save_block(m["path"], m["body"]))

    for m in matches:
        body = textwrap.dedent(m["body"]); lang = m["lang"].lower()
        res: str
        if lang == "python":
            res = _exec_python(body)
        elif lang == "bash":
            res = _exec_bash(body)
        else:
            tmp = f"__nested_{uuid.uuid4().hex}.md"
            (BASE_PATH / tmp).write_text(body, encoding="utf-8")
            res = run_md(tmp, depth=depth + 1, quiet=quiet)
        executed.append({"type": lang, "preview": res[:120]})

    _log(f"✅ mission {rel} completata – {len(written)} file / {len(executed)} blocchi")
    return json.dumps(
        {"mission": rel, "files_written": written,
         "blocks_executed": executed, "log": str(LOG_FILE.relative_to(BASE_PATH))},
        ensure_ascii=False, indent=2)

# ═════════════ CLI ═════════════════════════════════════════
if __name__ == "__main__":
    import argparse, time
    ap = argparse.ArgumentParser(description="Mercurius∞ Markdown runner")
    ap.add_argument("file", help="Path missione (relativo a BASE_PATH)")
    ap.add_argument("--quiet", action="store_true", help="niente DEBUG su stderr")
    args = ap.parse_args()

    t0 = time.perf_counter()
    print(run_md(args.file, quiet=args.quiet))
    print(f"-- finito in {time.perf_counter()-t0:.2f}s --")
