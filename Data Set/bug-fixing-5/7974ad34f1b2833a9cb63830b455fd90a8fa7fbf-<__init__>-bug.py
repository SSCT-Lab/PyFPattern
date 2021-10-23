def __init__(self):
    super(CallbackModule, self).__init__()
    if (not HAS_LOGSTASH):
        self.disabled = True
        self._display.warning('The required python-logstash is not installed. pip install python-logstash')
    else:
        self.logger = logging.getLogger('python-logstash-logger')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logstash.TCPLogstashHandler(os.getenv('LOGSTASH_SERVER', 'localhost'), int(os.getenv('LOGSTASH_PORT', 5000)), version=1, message_type=os.getenv('LOGSTASH_TYPE', 'ansible'))
        self.logger.addHandler(self.handler)
        self.hostname = socket.gethostname()
        self.session = str(uuid.uuid1())
        self.errors = 0