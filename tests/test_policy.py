# tests/test_policy.py
import pytest

pytest.skip("PolicyManager richiede dipendenze yaml", allow_module_level=True)

from safety.policy_manager import PolicyManager

def test_policy_block():
    mgr = PolicyManager()
    mgr.add_policy("no_secrets", "password=", "block")
    assert mgr.check("here is password=123")["name"] == "no_secrets"
