def __sub__(self, other):
    'x.__sub__(y) <=> x-y '
    if isinstance(other, Symbol):
        return _internal._Minus(self, other)
    if isinstance(other, Number):
        return _internal._MinusScalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))