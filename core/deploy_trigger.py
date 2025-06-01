# core/deploy_trigger.py
"""
Modulo: deploy_trigger.py
Descrizione: Orchestratore di update->test->deploy->validate.
"""

from updater.auto_updater import AutoUpdater
from deploy.env_checker import EnvChecker
from deploy.deployment_handler import DeploymentHandler
from deploy.rollout_validator import RolloutValidator

if __name__ == "__main__":
    checker = EnvChecker()
    assert checker.check_python(), "Python version incompatible."
    assert not checker.missing_packages(), "Missing core packages."

    updater = AutoUpdater(repo_url="https://github.com/giack891811/mercurius_infinite_final.git")
    print(updater.update("git"))

    deployer = DeploymentHandler()
    deployer.deploy_docker()

    validator = RolloutValidator()
    tests_ok = validator.run_tests()
    health = validator.check_health()
    print("✅ Deploy OK" if tests_ok and health["status"] else "❌ Deploy issues", health)
