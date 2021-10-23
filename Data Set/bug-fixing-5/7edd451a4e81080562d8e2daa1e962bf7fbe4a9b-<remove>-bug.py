def remove(self, module):
    weight = module._parameters[(self.name + '_org')]
    del module._parameters[self.name]
    del module._buffers[(self.name + '_u')]
    del module._parameters[(self.name + '_org')]
    module.register_parameter(self.name, weight)