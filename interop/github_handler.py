# interop/github_handler.py

"""
Modulo: github_handler.py
Descrizione: Gestione automatica della sincronizzazione con GitHub.
"""

from git import Repo, GitCommandError

class GitHubHandler:
    def __init__(self, repo_path: str = ".", remote_name: str = "origin"):
        self.repo = Repo(repo_path)
        self.remote = self.repo.remote(name=remote_name)

    def pull_latest(self):
        try:
            self.remote.pull()
            print("✅ Pull completato da GitHub.")
        except GitCommandError as e:
            print(f"❌ Errore durante il pull: {e}")

    def push_changes(self, commit_message: str = "🔄 Update automatico da Mercurius"):
        try:
            self.repo.git.add(A=True)
            self.repo.index.commit(commit_message)
            self.remote.push()
            print("🚀 Push effettuato con successo.")
        except GitCommandError as e:
            print(f"❌ Errore durante il push: {e}")
