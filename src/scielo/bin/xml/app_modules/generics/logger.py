
import logging


def get_logger(filename, logger_name, logging_level=logging.DEBUG):
    """
    CRITICAL    50
    ERROR   40
    WARNING     30
    INFO    20
    DEBUG   10
    NOTSET  0
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)

    # create a file handler
    handler = logging.FileHandler(filename)
    handler.setLevel(logging_level)

    # create a logging format
    formatter = logging.Formatter(
        u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger
