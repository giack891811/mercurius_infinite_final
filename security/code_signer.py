# security/code_signer.py

"""
Modulo: code_signer.py
Descrizione: Firma SHA256 con timestamp dei file generati da Mercurius∞.
Ogni file riceve un blocco firma in coda per verifica integrità e autenticità.
"""

import hashlib
import datetime


class CodeSigner:
    def __init__(self, author="Mercurius∞"):
        self.author = author

    def generate_signature(self, content: str) -> str:
        sha = hashlib.sha256(content.encode()).hexdigest()
        timestamp = datetime.datetime.utcnow().isoformat()
        return f"\n\n# --SIGNATURE--\n# SHA256: {sha}\n# SignedAt: {timestamp}\n# By: {self.author}\n"

    def sign_file(self, filepath: str):
        with open(filepath, "r") as f:
            code = f.read()
        signature = self.generate_signature(code)
        with open(filepath, "a") as f:
            f.write(signature)
        return f"✅ File firmato: {filepath}"
