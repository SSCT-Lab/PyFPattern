def __add__(self, other):
    'x.__add__(y) <=> x+y\n        Scalar input is supported.\n        Broadcasting is not supported. Use `broadcast_add` instead. '
    if isinstance(other, Symbol):
        return _internal._Plus(self, other)
    if isinstance(other, Number):
        return _internal._PlusScalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))