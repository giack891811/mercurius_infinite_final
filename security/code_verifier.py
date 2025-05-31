# security/code_verifier.py

"""
Modulo: code_verifier.py
Descrizione: Verifica la firma SHA256 di un file generato per garantirne l'integrità.
Estrae blocco firma e confronta l'hash del codice.
"""

import hashlib


class CodeVerifier:
    def verify_file(self, filepath: str) -> str:
        with open(filepath, "r") as f:
            lines = f.readlines()

        try:
            idx = lines.index("# --SIGNATURE--\n")
            code = "".join(lines[:idx])
            original_hash = [l for l in lines[idx:] if "SHA256" in l][0].split(":")[1].strip()
            actual_hash = hashlib.sha256(code.encode()).hexdigest()

            if actual_hash == original_hash:
                return "✅ Firma valida – contenuto integro"
            else:
                return "❌ Firma NON valida – file modificato"
        except Exception:
            return "⚠️ Firma non trovata o incompleta"
