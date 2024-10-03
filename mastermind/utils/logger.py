import logging

from .dir import Dir


def setup_logger(name: str, level=logging.DEBUG):
    """Génère un logger personnalisé"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(Dir.ROOT / "app.log", encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
