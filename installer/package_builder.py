# installer/package_builder.py

"""
Modulo: package_builder.py
Descrizione: Creazione automatica di eseguibili desktop Mercurius∞ per Windows, Linux, Mac.
"""

import os
import subprocess
from datetime import datetime

class PackageBuilder:
    def __init__(self, exports_dir="exports/"):
        self.exports_dir = exports_dir
        os.makedirs(exports_dir, exist_ok=True)

    def build_windows_exe(self, entry_script: str, icon: str = None):
        cmd = [
            "pyinstaller", "--onefile", "--noconsole", entry_script,
            "--distpath", self.exports_dir,
            "--name", "Mercurius"
        ]
        if icon:
            cmd += ["--icon", icon]
        self._run(cmd, "windows")

    def build_linux_sh(self, entry_script: str):
        output_file = os.path.join(self.exports_dir, "mercurius.sh")
        with open(output_file, "w") as f:
            f.write(f"#!/bin/bash\npython3 {entry_script}")
        os.chmod(output_file, 0o755)
        self._log_build("linux", output_file)

    def build_mac_app(self, entry_script: str):
        app_path = os.path.join(self.exports_dir, "Mercurius.app")
        os.makedirs(app_path, exist_ok=True)
        os.symlink(entry_script, os.path.join(app_path, "Mercurius"))
        self._log_build("mac", app_path)

    def _run(self, cmd, platform: str):
        try:
            subprocess.run(cmd, check=True)
            self._log_build(platform, self.exports_dir)
        except subprocess.CalledProcessError as e:
            print(f"❌ Errore durante build {platform}: {e}")

    def _log_build(self, platform: str, path: str):
        log_path = os.path.join(self.exports_dir, "README.txt")
        with open(log_path, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] Build completata ({platform}): {path}\n")
