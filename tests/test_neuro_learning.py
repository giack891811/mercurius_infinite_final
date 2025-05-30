"""Test base per motore di apprendimento visivo.""" 

from modules.Neo.neuro_learning_engine import parse_video_and_generate_knowledge

def test_video_learning():
    result = parse_video_and_generate_knowledge("Plasticità sinaptica")
    assert "concept" in result
    print("✅ Test neuro-learning passed")