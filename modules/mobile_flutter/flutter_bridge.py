"""Launcher for the Flutter-based mobile Jarvis UI."""
from __future__ import annotations

import subprocess
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent / "mobile_jarvis_ui"


def start_mobile_ui() -> None:
    """Attempt to launch the Flutter app."""
    flutter = shutil.which("flutter")
    if not flutter:
        print("⚠️ Flutter SDK not found. Please run the app manually from mobile_jarvis_ui.")
        return
    try:
        subprocess.Popen([flutter, "run", "-d", "android"], cwd=str(PROJECT_DIR))
        print("📱 Mobile Jarvis UI launched")
    except Exception as exc:
        print(f"⚠️ Unable to launch Flutter app: {exc}")
