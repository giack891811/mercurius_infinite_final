"""run_selfmission.py – HYPER v4.0-turbo | Mercurius∞
Potenziato con:
- RotatingFileHandler + colori ANSI (autoreset)
- Fix console Windows CP1252 (emoji safe)
- CLI avanzata (--all, --log-level, --no-color, --log-file, --max-depth)
- .env support (python-dotenv fallback)
- Traceback completo sempre loggato
"""

from __future__ import annotations

import io
import argparse
import json
import logging
import logging.handlers
import os
import re
import subprocess
import sys
import textwrap
import time
import traceback
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any, Dict, List, TypedDict

# ╔════════════╗
# ║  Config    ║
# ╚════════════╝
ENV_PATH = Path(".env")
if ENV_PATH.exists():
    # lazy import to avoid hard-dep se manca
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(dotenv_path=ENV_PATH)

def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / ".git").exists():
            return p
    return Path.cwd()

BASE_PATH = Path(os.getenv("MERCURIUS_BASE", repo_root()))
DEFAULT_LOG = BASE_PATH / "logs" / "selfmission_last.log"
DEFAULT_LOG.parent.mkdir(parents=True, exist_ok=True)

# regex compile
WRITE_RE = re.compile(
    r'write_file\(\s*"(?P<path>[^"]+)"\s*,\s*<<EOF\s*(?P<body>.*?)\s*EOF\)',
    re.I | re.S,
)
CODE_RE = re.compile(
    r"""^\s*```[ \t]*(?P<lang>python|bash|mission)[ \t]+run[ \t]*\r?\n
        (?P<body>.*?)\r?\n\s*```[ \t]*$""",
    re.I | re.S | re.M | re.X,
)

# ╔════════════╗
# ║  Logging   ║
# ╚════════════╝
def setup_logger(
    level: str = "INFO",
    log_file: Path = DEFAULT_LOG,
    use_color: bool = True,
) -> logging.Logger:
    fmt_plain = "%(asctime)s | %(levelname)-8s | %(message)s"
    fmt_color = "%(log_color)s" + fmt_plain

    logger = logging.getLogger("selfmission")
    logger.setLevel(level.upper())
    logger.handlers.clear()

    # rotating file
    file_h = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=int(os.getenv("MERCURIUS_LOG_MAX", 1_000_000)), backupCount=5, encoding="utf-8"
    )
    file_h.setFormatter(logging.Formatter(fmt_plain))
    logger.addHandler(file_h)

    # console
    console_h = logging.StreamHandler()
    if use_color and sys.stdout.isatty():
        try:
            from colorama import init as cinit  # :contentReference[oaicite:2]{index=2}
            from colorama import Fore, Style
            cinit(autoreset=True)
            class ColorFmt(logging.Formatter):
                def format(self, record):
                    colour = {
                        "INFO": Fore.GREEN,
                        "WARNING": Fore.YELLOW,
                        "ERROR": Fore.RED,
                        "CRITICAL": Fore.RED + Style.BRIGHT,
                        "DEBUG": Fore.CYAN,
                    }.get(record.levelname, "")
                    record.log_color = colour
                    return super().format(record)
            console_h.setFormatter(ColorFmt(fmt_color))
        except ImportError:
            console_h.setFormatter(logging.Formatter(fmt_plain))
    else:
        console_h.setFormatter(logging.Formatter(fmt_plain))
    logger.addHandler(console_h)
    return logger

LOG = setup_logger(
    level=os.getenv("MERCURIUS_LOG_LEVEL", "INFO"),
    use_color=os.getenv("MERCURIUS_NO_COLOR", "0") != "1",
)

# ╔════════════╗
# ║  Helpers   ║
# ╚════════════╝
def _safe_print(msg: str):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))

def _save_block(rel_path: str, body: str) -> str:
    dest = BASE_PATH / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")
    LOG.info("📝  write_file → %s (%d linee)", rel_path, len(body.splitlines()))
    return str(dest.relative_to(BASE_PATH))

def _exec_python(code: str, *, md_path: Path | None = None) -> str:
    """Esegue un blocco Python in-process e cattura stdout/stderr.

    Args:
        code:    sorgente Python da eseguire.
        md_path: percorso assoluto del file .md che contiene il blocco;
                 se passato, viene esportato come __file__ dentro exec().

    Returns:
        stdout + stderr prodotti dal blocco.
    """
    out, err = io.StringIO(), io.StringIO()
    t0 = time.perf_counter()

    # namespace dell’esecuzione
    ns: Dict[str, Any] = {"__name__": "__mission__"}
    if md_path is not None:
        ns["__file__"] = str(md_path)   # permette al codice di usare __file__

    try:
        with redirect_stdout(out), redirect_stderr(err):
            exec(code, ns)
    except Exception:
        traceback.print_exc(file=err)

    dt = time.perf_counter() - t0
    LOG.info("⚙️  python %.2fs • stdout=%dB • stderr=%dB",
             dt, len(out.getvalue()), len(err.getvalue()))

    if err.getvalue():
        LOG.error("TRACEBACK ↓\n%s", err.getvalue())

    return out.getvalue() + err.getvalue()


def _exec_bash(cmd: str) -> str:
    shell, use_shell = (["powershell", "-NoLogo", "-Command", cmd], False) if os.name == "nt" else (cmd, True)
    proc = subprocess.run(shell, shell=use_shell, capture_output=True, text=True,
                          cwd=BASE_PATH, timeout=60)
    LOG.info("⚙️  bash rc=%d • stdout=%dB • stderr=%dB", proc.returncode, len(proc.stdout), len(proc.stderr))
    if proc.stderr:
        LOG.error("BASH-ERR ↓\n%s", proc.stderr)
    return proc.stdout + proc.stderr

# ╔════════════╗
# ║  Runner    ║
# ╚════════════╝
class ExecSummary(TypedDict):
    type: str
    preview: str

def run_md(path: str, *, depth=0, max_depth=3, quiet=False) -> str:
    if depth > max_depth:
        return "[ABORT] Ricorsione troppo profonda"
    md_path = BASE_PATH / path
    if not md_path.exists():
        return f"[ERRORE] File non trovato: {path}"

    text = md_path.read_text(encoding="utf-8", errors="replace")
    matches = list(CODE_RE.finditer(text))
    if not quiet:
        LOG.debug("DEBUG ‣ %s blocchi=%d", path, len(matches))
    if not matches:
        return "[ERRORE] 0 blocchi trovati – controlla il Markdown"

    written: List[str] = []
    executed: List[ExecSummary] = []

    for m in WRITE_RE.finditer(text):
        written.append(_save_block(m["path"], m["body"]))

    for m in matches:
        lang = m["lang"].lower()
        body = textwrap.dedent(m["body"])
        if lang == "python":
            res = _exec_python(body)
        elif lang == "bash":
            res = _exec_bash(body)
        else:
            tmp = f"__nested_{uuid.uuid4().hex}.md"
            (BASE_PATH / tmp).write_text(body, encoding="utf-8")
            res = run_md(tmp, depth=depth + 1, max_depth=max_depth, quiet=quiet)
        executed.append({"type": lang, "preview": res[:160].replace("\n", " ")})

    LOG.info("✅  mission %s completata – %d file / %d blocchi", path, len(written), len(executed))
    return json.dumps(
        {"mission": path, "files_written": written,
         "blocks_executed": executed,
         "log": str(DEFAULT_LOG.relative_to(BASE_PATH))},
        ensure_ascii=False, indent=2)

# ╔════════════╗
# ║   CLI      ║
# ╚════════════╝
def cli() -> None:
    p = argparse.ArgumentParser(description="Mercurius∞ Markdown runner")
    p.add_argument("file", nargs="?", help="Missione singola (.md) o cartella con --all")
    p.add_argument("--all", action="store_true", help="Esegui tutte le .md sotto path/cartella")
    p.add_argument("--quiet", action="store_true", help="Silenzia DEBUG")
    p.add_argument("--no-color", action="store_true", help="Disabilita colori ANSI")
    p.add_argument("--log-file", type=Path, default=DEFAULT_LOG, help="Percorso log")
    p.add_argument("--log-level", default="INFO", help="DEBUG, INFO, WARNING…")
    p.add_argument("--max-depth", type=int, default=3, help="Profondità ricorsione mission annidate")
    args = p.parse_args()

    # re-inizializza logger se servono opzioni CLI
    global LOG
    LOG = setup_logger(args.log_level, args.log_file, not args.no_color)

    targets: List[Path]
    base = Path(args.file or "missions")
    if args.all:
        targets = list(base.rglob("*.md"))
    else:
        targets = [base]

    t0 = time.perf_counter()
    for t in targets:
        try:
            rel_path = t.relative_to(BASE_PATH)   # usa relativo se è nel repo
        except ValueError:
            rel_path = t                          # altrimenti mantieni l’assoluto
        _safe_print(run_md(str(rel_path),
                           quiet=args.quiet,
                           max_depth=args.max_depth))
    LOG.info("-- finito in %.2fs --", time.perf_counter() - t0)

if __name__ == "__main__":
    # Fix Windows console cp1252 → UTF-8 solo per questa sessione
    if os.name == "nt" and "PYTHONIOENCODING" not in os.environ:
        os.environ["PYTHONIOENCODING"] = "utf-8"
    cli()
