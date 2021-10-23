def set_default_param_initializer(self):
    '\n        Set the default initializer for the parameter with Xavier.\n\n        Args:\n            None.\n\n        Returns:\n            None.\n        '
    self.set_default_initializer(Xavier())