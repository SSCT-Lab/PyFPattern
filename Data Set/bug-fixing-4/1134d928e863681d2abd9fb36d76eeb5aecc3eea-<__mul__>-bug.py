def __mul__(self, other):
    'x.__mul__(y) <=> x*y '
    if isinstance(other, Symbol):
        return _internal._Mul(self, other)
    if isinstance(other, Number):
        return _internal._MulScalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))