# security/pairing_manager.py

"""
Modulo: pairing_manager.py
Descrizione: Gestione pairing sicuro con utente tramite QR code o password vocale.
"""

import qrcode
from voice.stt import transcribe_audio


def generate_qr_pairing_link(link: str, filename: str = "pairing_qr.png") -> None:
    """
    Genera un QR code da un link e lo salva come immagine.
    """
    img = qrcode.make(link)
    img.save(filename)
    print(f"✅ QR generato: {filename}")


def pair_with_user(method: str = "qr") -> bool:
    """
    Esegue il pairing con l'utente. Metodo supportato: 'qr', 'voice'
    """
    if method == "qr":
        generate_qr_pairing_link("https://mercurius.local/pair")
        return True

    elif method == "voice":
        print("🔒 Pronuncia la password vocale:")
        spoken = transcribe_audio().lower()
        return "mercurius autorizza" in spoken

    return False
