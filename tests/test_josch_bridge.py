from integrations.bridge_josch import send_command_to_pc

def test_send_command_format():
    resp = send_command_to_pc("echo test")
    assert isinstance(resp, dict)
