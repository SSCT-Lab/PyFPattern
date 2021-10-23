def set_default_bias_initializer(self):
    '\n        Set the default initializer for the bias with Constant(0.0).\n\n        Args:\n            None.\n\n        Returns:\n            None.\n        '
    self.set_default_initializer(Constant(0.0))