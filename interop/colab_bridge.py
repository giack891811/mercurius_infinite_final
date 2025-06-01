# interop/colab_bridge.py

"""
Modulo: colab_bridge.py
Descrizione: Rilevamento ed estensione delle capacità di esecuzione su Google Colab.
"""

import os

def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

def setup_drive():
    if is_colab():
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Google Drive montato.")
