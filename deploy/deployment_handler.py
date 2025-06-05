# deploy/deployment_handler.py
"""
Modulo: deployment_handler.py
Descrizione: Gestisce il deploy di Mercurius∞ su:
• locale Docker
• remoto SSH
• Google Colab (zip upload)
"""

import subprocess
import paramiko
from analytics.behavior_logger import BehaviorLogger

log = BehaviorLogger()


class DeploymentHandler:
    def __init__(self):
        pass

    def deploy_docker(self):
        res = subprocess.run(["docker", "compose", "up", "-d", "--build"], capture_output=True, text=True)
        log.log("deploy", {"target": "docker", "stdout": res.stdout, "stderr": res.stderr})
        return res.returncode == 0

    def deploy_ssh(self, host: str, user: str, key_path: str, target_dir: str):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, key_filename=key_path)
        cmd = f"cd {target_dir} && git pull && docker compose up -d --build"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        ssh.close()
        log.log("deploy", {"target": host, "stdout": out, "stderr": err})
        return err == ""
