"""
logger.py
=========
Configurazione logging per il sistema Mercurius∞.
"""

import logging
import os

def setup_logger(name: str = "MercuriusLogger", logfile: str = "logs/execution.log"):
    """Return a console+file logger"""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if logfile:
            os.makedirs(os.path.dirname(logfile), exist_ok=True)
            fh = logging.FileHandler(logfile, encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
    return logger

def get_file_logger(name="MercuriusFileLogger", filename="mercurius.log"):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(filename, encoding="utf-8")
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
