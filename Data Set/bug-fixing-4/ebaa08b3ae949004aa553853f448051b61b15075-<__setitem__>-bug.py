def __setitem__(self, index, value):
    'Set the coordinate sequence value at the given index.'
    if isinstance(value, (list, tuple)):
        pass
    elif (numpy and isinstance(value, numpy.ndarray)):
        pass
    else:
        raise TypeError('Must set coordinate with a sequence (list, tuple, or numpy array).')
    if ((self.dims == 3) and self._z):
        n_args = 3
        set_3d = True
    else:
        n_args = 2
        set_3d = False
    if (len(value) != n_args):
        raise TypeError('Dimension of value does not match.')
    self.setX(index, value[0])
    self.setY(index, value[1])
    if set_3d:
        self.setZ(index, value[2])