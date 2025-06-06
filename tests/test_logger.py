from utils.logger import setup_logger


def test_setup_logger():
    logger = setup_logger("test_logger")
    logger.info("log message")
    assert logger.name == "test_logger"
