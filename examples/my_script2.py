# examples/myscript2.py
import logging

logger = logging.getLogger(__name__)


def do_stuff2():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

    try:
        x = 1 / 0
    except:
        logger.exception('This is an exception')
