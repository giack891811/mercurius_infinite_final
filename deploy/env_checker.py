# deploy/env_checker.py
"""
Modulo: env_checker.py
Descrizione: Verifica versioni Python, dipendenze, GPU/CPU per deployment sicuro.
"""

import importlib
import platform
import subprocess
import pkg_resources
from typing import List, Dict


class EnvChecker:
    MIN_PY = (3, 9)
    REQUIRED_PKGS = ["torch", "openai", "fastapi"]

    def summary(self) -> Dict[str, str]:
        return {
            "python": platform.python_version(),
            "system": platform.system(),
            "machine": platform.machine(),
        }

    def check_python(self) -> bool:
        return tuple(int(i) for i in platform.python_version_tuple()[:2]) >= self.MIN_PY

    def missing_packages(self) -> List[str]:
        missing = []
        for pkg in self.REQUIRED_PKGS:
            try:
                importlib.import_module(pkg)
            except ImportError:
                missing.append(pkg)
        return missing

    def gpu_info(self) -> str:
        try:
            res = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"])
            return res.decode().strip()
        except Exception:
            return "No NVIDIA GPU found"
