# build_dashboard.py
"""
Script: build_dashboard.py
Uso: genera un eseguibile standalone per il modulo dashboard.py
"""

import os

ENTRY = "dashboard.py"
ICON = "icon/icon.ico"

os.system(f"pyinstaller --onefile --windowed --icon={ICON} --name=MercuriusGUI {ENTRY}")
