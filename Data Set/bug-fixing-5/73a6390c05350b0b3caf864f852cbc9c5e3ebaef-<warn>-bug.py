def warn(self):
    if self.urgent:
        type = 'import'
    else:
        type = 'use'
    message = ('%s %s: %s' % (type, self.name, self.info))
    if self.reason:
        message += ('\n(%s)' % self.reason)
    try:
        import warnings
        if self.urgent:
            level = 4
        else:
            level = 3
        warnings.warn(message, RuntimeWarning, level)
    except ImportError:
        print(message)