from logging.config import ConvertingList, ConvertingDict, valid_ident
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
import atexit


def _resolve_handlers(l):
    if not isinstance(l, ConvertingList):
        return l

    # Indexing the list performs the evaluation.
    resolved_handlers = []
    for i in range(len(l)):
        handler = l[i]
        if isinstance(handler, dict) and handler.get('class') == 'logging.StreamHandler':
            # Create the StreamHandler manually
            stream_handler = logging.StreamHandler(stream=handler['stream'])
            stream_handler.setLevel(handler.get('level', logging.NOTSET))
            if 'formatter' in handler:
                stream_handler.setFormatter(handler['formatter'])
            handler = stream_handler
        resolved_handlers.append(handler)
    return resolved_handlers


def _resolve_queue(q):
    if not isinstance(q, ConvertingDict):
        return q
    if '__resolved_value__' in q:
        return q['__resolved_value__']

    cname = q.pop('class')
    klass = q.configurator.resolve(cname)
    props = q.pop('.', None)
    kwargs = {k: q[k] for k in q if valid_ident(k)}
    result = klass(**kwargs)
    if props:
        for name, value in props.items():
            setattr(result, name, value)

    q['__resolved_value__'] = result
    return result


class QueueListenerHandler(QueueHandler):

    def __init__(self, handlers, respect_handler_level=False, auto_run=True, queue=Queue(-1)):
        queue = _resolve_queue(queue)
        super().__init__(queue)
        handlers = _resolve_handlers(handlers)
        self._listener = QueueListener(
            self.queue,
            *handlers,
            respect_handler_level=respect_handler_level)
        if auto_run:
            self.start()
            atexit.register(self.stop)

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()

    def emit(self, record):
        return super().emit(record)
