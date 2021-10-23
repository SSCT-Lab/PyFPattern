def __getattr__(self, var):
    if (not self.urgent):
        self.warn()
        self.urgent = 1
    missing_msg = ('%s module not available (%s)' % (self.name, self.reason))
    raise NotImplementedError(missing_msg)