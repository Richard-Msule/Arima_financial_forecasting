import logging
from logging import FileHandler
from logging import Formatter
from logging import StreamHandler

LOG_FORMAT_CONSOLE = ("%(asctime)s %(levelname)s: %(message)s")
LOG_FORMAT_FILE = ("%(asctime)s, %(message)s")
LOG_LEVEL = logging.INFO

INFO = logging.INFO
DEBUG = logging.DEBUG

def  get_console_logger(name, level = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream = StreamHandler()
    stream.setFormatter(Formatter(LOG_FORMAT_CONSOLE))
    logger.addHandler(stream)
    return logger

def  get_file_logger(name, filename):
    if filename != None:
        logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL)
        file_handler = FileHandler(filename, mode='w')
        file_handler.setFormatter(Formatter(LOG_FORMAT_FILE))
        logger.addHandler(file_handler)
        return logger
    else:
        return None
