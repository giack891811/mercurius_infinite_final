from modules.GPT.gpt_runner import run_gpt


def test_run_gpt():
    result = run_gpt("ciao")
    assert result.startswith("GPT>")
