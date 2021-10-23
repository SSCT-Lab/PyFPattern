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
        point_setter = self._set_point_3d
    else:
        n_args = 2
        point_setter = self._set_point_2d
    if (len(value) != n_args):
        raise TypeError('Dimension of value does not match.')
    self._checkindex(index)
    point_setter(index, value)