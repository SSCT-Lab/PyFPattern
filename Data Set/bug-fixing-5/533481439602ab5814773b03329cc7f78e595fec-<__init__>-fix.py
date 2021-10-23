def __init__(self):
    super(CallbackModule, self).__init__()
    self.logger = logging.getLogger('ansible logger')
    self.logger.setLevel(logging.DEBUG)
    self.handler = logging.handlers.SysLogHandler(address=(os.getenv('SYSLOG_SERVER', 'localhost'), int(os.getenv('SYSLOG_PORT', 514))), facility=os.getenv('SYSLOG_FACILITY', logging.handlers.SysLogHandler.LOG_USER))
    self.logger.addHandler(self.handler)
    self.hostname = socket.gethostname()