def set_default_bias_initializer(self):
    self.set_default_initializer(Constant(0.0))