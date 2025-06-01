# updater/auto_updater.py
"""
Modulo: auto_updater.py
Descrizione: Aggiorna Mercurius∞ da remoto (GitHub) o da pacchetto tar/zip.
• Scarica la nuova versione
• Esegue migrazioni (requirements, db)
• Riavvia il processo principale
"""

import subprocess
import sys
from pathlib import Path
from typing import Literal, Optional
from analytics.behavior_logger import BehaviorLogger

logger = BehaviorLogger()


class AutoUpdater:
    def __init__(self, repo_url: str, branch: str = "main"):
        self.repo_url = repo_url
        self.branch = branch
        self.repo_dir = Path(".").resolve()

    # ---------- public ----------
    def update(self, source: Literal["git", "package"] = "git", pkg_file: Optional[str] = None):
        if source == "git":
            return self._pull_git()
        if source == "package" and pkg_file:
            return self._extract_package(pkg_file)
        raise ValueError("Sorgente update non valida.")

    # ---------- internal ----------
    def _pull_git(self):
        cmd = ["git", "pull", self.repo_url, self.branch]
        res = subprocess.run(cmd, cwd=self.repo_dir, text=True, capture_output=True)
        logger.log("auto_update", {"method": "git", "stdout": res.stdout, "stderr": res.stderr})
        if res.returncode == 0:
            self._post_update()
            return "✅ Update da Git completato."
        return f"❌ Git pull error: {res.stderr}"

    def _extract_package(self, pkg_file: str):
        import tarfile, zipfile, shutil, tempfile

        tmp = Path(tempfile.mkdtemp())
        if pkg_file.endswith(".tar.gz"):
            with tarfile.open(pkg_file) as tar:
                tar.extractall(tmp)
        elif pkg_file.endswith(".zip"):
            with zipfile.ZipFile(pkg_file) as zf:
                zf.extractall(tmp)
        else:
            return "Formato pacchetto non supportato."

        # Copia sopra il codice
        for item in tmp.iterdir():
            target = self.repo_dir / item.name
            if target.exists():
                shutil.rmtree(target, ignore_errors=True)
            shutil.move(item, target)
        logger.log("auto_update", {"method": "package", "file": pkg_file})
        self._post_update()
        return "✅ Update da package completato."

    def _post_update(self):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        logger.log("auto_update", {"action": "deps_installed"})
