def __getattr__(self, var):
    if (not self.urgent):
        self.warn()
        self.urgent = 1
    MissingPygameModule = ('%s module not available' % self.name)
    if self.reason:
        MissingPygameModule += ('\n(%s)' % self.reason)
    raise NotImplementedError(MissingPygameModule)