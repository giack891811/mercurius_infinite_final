import subprocess
import platform
import datetime

class LeonAI:
    def __init__(self):
        self.os_type = platform.system()
        print(f"🦾 LeonAI avviato su: {self.os_type}")

    def esegui_comando(self, comando: str) -> str:
        # Sicurezza: blocca comandi potenzialmente pericolosi
        proibiti = ["rm", "del", "shutdown", "format", "mkfs", "dd", ">", ":", "sudo", "su"]
        if any(x in comando for x in proibiti):
            raise PermissionError("❌ Comando pericoloso bloccato da LeonAI.")
        try:
            result = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, timeout=15, text=True)
            self._log(comando, result)
            return result
        except subprocess.CalledProcessError as e:
            self._log(comando, e.output)
            return f"❌ Errore comando: {e.output}"
        except Exception as ex:
            self._log(comando, str(ex))
            return f"❌ Errore generale: {str(ex)}"

    def _log(self, comando, output):
        with open("logs/leonai_commands.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] CMD: {comando}\nOUTPUT:\n{output}\n{'='*50}\n")

if __name__ == "__main__":
    ai = LeonAI()
    while True:
        cmd = input("LeonAI$ ")
        try:
            print(ai.esegui_comando(cmd))
        except Exception as ex:
            print(f"[LeonAI] Errore: {ex}")
