from modules.sandbox_executor.secure_executor import SecureExecutor

def test_successful_execution():
    executor = SecureExecutor(timeout=2)
    result = executor.execute("x = 1 + 1\nprint(x)")
    assert "2" in result["output"]
    assert result["error"] == ""
    assert result["stderr"] == ""

def test_timeout_execution():
    executor = SecureExecutor(timeout=1)
    result = executor.execute("while True: pass")
    assert result["error"] == "Execution timed out."

def test_error_handling():
    executor = SecureExecutor()
    result = executor.execute("raise ValueError('Errore di test')")
    assert "ValueError" in result["error"]
