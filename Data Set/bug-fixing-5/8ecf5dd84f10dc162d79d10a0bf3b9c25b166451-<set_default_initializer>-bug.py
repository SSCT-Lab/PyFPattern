def set_default_initializer(self, initializer):
    if (initializer is None):
        if (self.initializer is None):
            raise ValueError('ParamAttr.initializer is not set')
        return
    if (self.initializer is not None):
        return
    self.initializer = initializer