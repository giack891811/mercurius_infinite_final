# security/gpg_support.py

"""
Modulo: gpg_support.py
Descrizione: Firma/verifica file tramite GPG. Richiede GnuPG installato.
"""

import subprocess


class GPGSupport:
    def gpg_sign_file(self, path: str, key_id: str) -> str:
        cmd = f"gpg --default-key {key_id} --output {path}.sig --detach-sig {path}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            return f"✅ File firmato con GPG: {path}.sig"
        except Exception as e:
            return f"❌ Errore GPG: {e}"

    def gpg_verify(self, path: str) -> str:
        cmd = f"gpg --verify {path}.sig {path}"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return f"❌ Verifica fallita: {e}"
