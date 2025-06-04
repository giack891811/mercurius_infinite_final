# tests/test_memory.py
import os
import tempfile
from memory.long_term_memory import LongTermMemory

def test_save_and_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = os.path.join(tmpdir, "test_exp.json")
        mem = LongTermMemory(json_path)
        mem.save_experience({"tags": ["unit"], "result": "ok"})
        data = mem.get_all()
        assert data and "tags" in data[-1]
