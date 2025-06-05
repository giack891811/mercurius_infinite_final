"""
Modulo: colab_bridge.py
Descrizione: Rilevamento ed estensione delle capacità di esecuzione su Google Colab.
"""

def is_colab():
    try:
        import google.colab as _
        return True
    except ImportError:
        return False

def setup_drive():
    if is_colab():
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Google Drive montato.")
    else:
        print("⚠️ Non in ambiente Colab: salto montaggio Drive.")

if __name__ == "__main__":
    setup_drive()
