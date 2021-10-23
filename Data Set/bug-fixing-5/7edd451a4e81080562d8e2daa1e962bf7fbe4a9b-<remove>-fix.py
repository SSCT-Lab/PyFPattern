def remove(self, module):
    weight = module._parameters[(self.name + '_org')]
    delattr(module, self.name)
    delattr(module, (self.name + '_u'))
    delattr(module, (self.name + '_org'))
    module.register_parameter(self.name, weight)