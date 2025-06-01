# modules/gpt_engineer_wrapper.py

"""
Modulo: gpt_engineer_wrapper.py
Descrizione: Interfaccia per pilotare GPT-Engineer via CLI o API, permettendo generazione autonoma di progetti e moduli.
"""

import subprocess
import os

class GPTEngineerWrapper:
    def __init__(self, project_path="generated_projects/", config_file=None):
        self.project_path = project_path
        self.config_file = config_file or "gpt_config.yaml"

    def generate_project(self, prompt: str) -> str:
        """
        Avvia GPT-Engineer per generare un progetto in base al prompt.
        """
        try:
            os.makedirs(self.project_path, exist_ok=True)
            with open("prompt.txt", "w") as f:
                f.write(prompt)

            result = subprocess.run(
                ["gpt-engineer", "."],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            return result.stdout or "✅ Generazione completata."
        except Exception as e:
            return f"❌ Errore GPT-Engineer: {e}"


# Test
if __name__ == "__main__":
    wrapper = GPTEngineerWrapper()
    print(wrapper.generate_project("Crea un'applicazione per il tracciamento del sonno"))
