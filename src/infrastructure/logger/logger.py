import logging
from logging.handlers import RotatingFileHandler

from src.infrastructure.logger.interfaces import ILogger


class Logger(ILogger):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.__logger = logging.getLogger()
        self.__logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler = RotatingFileHandler(
            filename='logs/logs.log',
            mode='w',
            maxBytes=1048576,
            backupCount=2
        )
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)

    def info(self, message):
        self.__logger.info(message)

    def error(self, message, exc_info=True):
        self.__logger.error(message, exc_info=exc_info)

    def warning(self, message):
        self.__logger.warning(message)

    def debug(self, message):
        self.__logger.debug(message)
