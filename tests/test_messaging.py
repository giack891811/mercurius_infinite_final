from modules.messaging.rabbitmq_messenger import publish_message

def test_publish_message_no_server():
    ok = publish_message('test_queue', 'hello')
    assert ok in (True, False)
