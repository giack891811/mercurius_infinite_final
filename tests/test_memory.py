# tests/test_memory.py
from memory.long_term_memory import LongTermMemory

def test_save_and_load():
    mem = LongTermMemory("test_exp.json")
    mem.save_experience({"tags": ["unit"], "result": "ok"})
    data = mem.get_all()
    assert data and "tags" in data[-1]
