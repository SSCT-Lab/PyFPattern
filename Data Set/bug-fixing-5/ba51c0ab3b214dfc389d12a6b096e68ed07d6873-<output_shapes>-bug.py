@property
def output_shapes(self):
    'Get output shapes.\n        Returns\n        -------\n        A list of `(name, shape)` pairs.\n        '
    assert self.binded
    return self._curr_module.label_shapes