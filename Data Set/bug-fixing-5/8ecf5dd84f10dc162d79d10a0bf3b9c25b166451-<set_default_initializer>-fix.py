def set_default_initializer(self, initializer):
    '\n        Set the default initializer, the initializer should be Constant,\n        Uniform, Normal, Xavier, MSRA.\n\n        Args:\n            initializer(Initializer): the initializer to set.\n\n        Returns:\n            None\n        '
    if (initializer is None):
        if (self.initializer is None):
            raise ValueError('ParamAttr.initializer is not set')
        return
    if (self.initializer is not None):
        return
    self.initializer = initializer