import logging
import logging.config
import yaml
from examples.my_script1 import do_stuff1
from examples.my_script2 import do_stuff2

LOGGING_CONFIG = """
version: 1
objects:
  queue:
    class: queue.Queue
    maxsize: 1000
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
    filename: 'config_example2.log'
    formatter: simple
  queue_listener:
    class: examples.QueueListenerHandler
    handlers:
      - cfg://handlers.console
      - cfg://handlers.file
    queue: cfg://objects.queue
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

logging_config = yaml.load(LOGGING_CONFIG, Loader=yaml.FullLoader)

logging.config.dictConfig(logging_config)

other_logger = logging.getLogger("foo")

do_stuff1()
do_stuff2()

other_logger.debug("A different debug message")
other_logger.info("A different info message")
other_logger.error("A different error message")
