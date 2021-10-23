

def __repr__(self):
    s = '{name}({mapping}, {_layout}'
    if (self._num_layers != 1):
        s += ', num_layers={_num_layers}'
    if (self._dropout != 0):
        s += ', dropout={_dropout}'
    if (self._dir == 2):
        s += ', bidirectional'
    s += ')'
    shape = self.i2h_weight[0].shape
    mapping = '{0} -> {1}'.format((shape[1] if shape[1] else None), (shape[0] / self._gates))
    return s.format(name=self.__class__.__name__, mapping=mapping, **self.__dict__)
