# security/code_signer.py

"""
Modulo: code_signer.py
Autore: Mercurius∞
Descrizione: Sistema di firma digitale SHA256 per tutti i file generati, con registrazione in log e firma visibile in coda al file.
"""

import hashlib
import json
from datetime import datetime
import os


class CodeSigner:
    def __init__(self, author="Mercurius∞", log_path="logs/code_signatures.json"):
        self.author = author
        self.log_path = log_path
        self.signatures = self.load_signatures()

    def load_signatures(self) -> dict:
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_signatures(self):
        with open(self.log_path, "w") as f:
            json.dump(self.signatures, f, indent=2)

    def generate_signature_block(self, content: str) -> str:
        sha = hashlib.sha256(content.encode()).hexdigest()
        timestamp = datetime.utcnow().isoformat()
        return f"\n\n# --SIGNATURE--\n# SHA256: {sha}\n# SignedAt: {timestamp}\n# By: {self.author}\n"

    def generate_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(block)
        return sha256_hash.hexdigest()

    def sign_file(self, file_path: str) -> str:
        # Legge contenuto originale
        with open(file_path, "r") as f:
            content = f.read()

        # Genera firma visibile
        signature_block = self.generate_signature_block(content)

        # Aggiunge firma al file
        with open(file_path, "a") as f:
            f.write(signature_block)

        # Log firma in file JSON
        file_hash = self.generate_hash(file_path)
        self.signatures[file_path] = {
            "file": file_path,
            "hash": file_hash,
            "timestamp": datetime.utcnow().isoformat(),
            "author": self.author
        }
        self.save_signatures()
        return f"✅ File firmato e registrato: {file_path}"

    def verify_signature(self, file_path: str) -> bool:
        if file_path not in self.signatures:
            return False
        current_hash = self.generate_hash(file_path)
        stored_hash = self.signatures[file_path]["hash"]
        return current_hash == stored_hash

    def report_signature_status(self, file_path: str) -> str:
        if self.verify_signature(file_path):
            info = self.signatures[file_path]
            return (f"🔐 Firma verificata:\n"
                    f"🗂 File: {info['file']}\n"
                    f"🕒 Timestamp: {info['timestamp']}\n"
                    f"🧑‍💻 Autore: {info['author']}\n"
                    f"🔑 SHA256: {info['hash']}")
        return "❌ Firma non valida o assente."

