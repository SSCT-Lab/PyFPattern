def __call__(self, module, inputs):
    (weight, u) = self.compute_weight(module)
    setattr(module, self.name, weight)
    setattr(module, (self.name + '_u'), u)