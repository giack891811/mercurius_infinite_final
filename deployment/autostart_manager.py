# deployment/autostart_manager.py

"""
Modulo: autostart_manager.py
Descrizione: Configura l'avvio automatico di Mercurius∞ come servizio persistente.
Supporta Linux (systemd), macOS (launchd), Windows (Task Scheduler).
"""

import os
import platform
import subprocess
import logging

logging.basicConfig(level=logging.INFO)


class AutoStartManager:
    def __init__(self, exec_path="main.py"):
        self.exec_path = os.path.abspath(exec_path)
        self.system = platform.system()

    def setup_autostart(self):
        if self.system == "Linux":
            return self._linux_systemd_service()
        elif self.system == "Darwin":
            return self._macos_launchd()
        elif self.system == "Windows":
            return self._windows_task_scheduler()
        else:
            return "[❌] Sistema operativo non supportato."

    def _linux_systemd_service(self):
        service_name = "mercurius.service"
        service_path = f"/etc/systemd/system/{service_name}"
        content = f"""[Unit]
Description=Mercurius AI Boot Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 {self.exec_path}
WorkingDirectory={os.path.dirname(self.exec_path)}
Restart=always
User={os.getenv("USER") or "pi"}

[Install]
WantedBy=multi-user.target
"""

        try:
            with open("/tmp/" + service_name, "w") as f:
                f.write(content)
            subprocess.run(["sudo", "mv", f"/tmp/{service_name}", service_path], check=True)
            subprocess.run(["sudo", "systemctl", "daemon-reexec"])
            subprocess.run(["sudo", "systemctl", "enable", service_name])
            subprocess.run(["sudo", "systemctl", "start", service_name])
            return f"[✅] Servizio avviato su systemd: {service_name}"
        except Exception as e:
            return f"[❌] Errore systemd: {e}"

    def _macos_launchd(self):
        plist_name = "com.mercurius.autostart.plist"
        plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{plist_name}")
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mercurius.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{self.exec_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>{os.path.dirname(self.exec_path)}</string>
</dict>
</plist>
"""

        try:
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            with open(plist_path, "w") as f:
                f.write(content)
            subprocess.run(["launchctl", "load", plist_path])
            return "[✅] Launchd configurato per macOS."
        except Exception as e:
            return f"[❌] Errore Launchd: {e}"

    def _windows_task_scheduler(self):
        try:
            task_name = "MercuriusBoot"
            cmd = f'schtasks /Create /SC ONLOGON /TN {task_name} /TR "python {self.exec_path}" /RL HIGHEST /F'
            subprocess.run(cmd, shell=True, check=True)
            return "[✅] Task creato in Windows Scheduler."
        except Exception as e:
            return f"[❌] Errore Scheduler: {e}"
