"""A queue listener for Python 3.12"""

from logging.handlers import QueueListener


class AutoStartQueueListener(QueueListener):

    def __init__(self, queue, *handlers, respect_handler_level=False):
        super().__init__(queue, *handlers, respect_handler_level=respect_handler_level)
        # Start the listener immediately.
        self.start()
