def warn(self):
    msg_type = ('import' if self.urgent else 'use')
    message = ('%s %s: %s\n(%s)' % (msg_type, self.name, self.info, self.reason))
    try:
        import warnings
        level = (4 if self.urgent else 3)
        warnings.warn(message, RuntimeWarning, level)
    except ImportError:
        print(message)