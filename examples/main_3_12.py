"""An example of configuring the logging queue handler for Python 3.12

In Python 3.12 support was add for configuring the queue handler. However
to make this work the `start` method on the `logging.handler.QueueListener`
must be called. This script shows how to do this by using a wrapper class,
and by getting the handler directly.
"""

import logging
import logging.config
import yaml
from examples.my_script1 import do_stuff1
from examples.my_script2 import do_stuff2

LOGGING_CONFIG = """
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    filename: 'config_example_3_12.log'
    formatter: simple
  queue_listener:
    class: logging.handlers.QueueHandler
    listener: examples.queue_listener_3_12.AutoStartQueueListener
    queue:
      (): queue.Queue
      maxsize: 1000
    level: DEBUG
    handlers:
      - console
      - file
loggers:
  examples.my_script1:
    level: DEBUG
    handlers:
      - queue_listener
    propagate: false
  examples.my_script2:
    level: WARNING
    handlers: 
      - queue_listener
    propagate: false
root:
  level: WARN
  handlers:
    - console"""


def main():
    logging_config = yaml.load(LOGGING_CONFIG, Loader=yaml.FullLoader)

    logging.config.dictConfig(logging_config)

    # We could start the listener directly.
    # handler = logging.getHandlerByName("queue_listener")
    # handler.listener.start()

    other_logger = logging.getLogger("foo")

    do_stuff1()
    do_stuff2()

    other_logger.debug("A different debug message")
    other_logger.info("A different info message")
    other_logger.error("A different error message")


if __name__ == '__main__':
    main()
