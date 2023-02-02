"""Logging helpers"""
import sys
import logging
from time import time
from functools import wraps


def get_logger(name: str):
    """Create named logger instance"""
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    logger.setLevel("INFO")
    handler.setFormatter(
        logging.Formatter(
            fmt='{"time": "%(asctime)s",'
            ' "module": "%(name)s",'
            ' "level": "%(levelname)s",'
            ' "message": "%(message)s"}',
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )
    logger.addHandler(handler)
    return logger


def timeit(function):
    """Log execution time"""
    logger = get_logger(function.__module__)

    @wraps(function)
    def wrap(*args, **kwargs):
        try:
            start = time()
            result = function(*args, **kwargs)
        finally:
            finish = time()
            logger.info(
                "call %r took %2.4f sec",
                function.__name__,
                finish - start,
            )
        return result

    return wrap