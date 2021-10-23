def __init__(self, name, urgent=0):
    self.name = name
    (exc_type, exc_msg) = sys.exc_info()[:2]
    self.info = str(exc_msg)
    self.reason = ('%s: %s' % (exc_type.__name__, self.info))
    self.urgent = urgent
    if urgent:
        self.warn()