def __init__(self, name, info='', urgent=0):
    self.name = name
    self.info = str(info)
    try:
        exc = sys.exc_info()
        if (exc[0] != None):
            self.reason = ('%s: %s' % (exc[0].__name__, str(exc[1])))
        else:
            self.reason = ''
    finally:
        del exc
    self.urgent = urgent
    if urgent:
        self.warn()