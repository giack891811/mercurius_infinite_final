from modules.llm.azr_reasoner import validate_with_azr


def test_validate_success():
    code = "x = 1\ny = x + 2"
    assert validate_with_azr(code) is True


def test_validate_failure():
    bad_code = "for"
    assert validate_with_azr(bad_code) is False
