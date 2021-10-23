def __div__(self, other):
    'x.__div__(y) <=> x/y '
    if isinstance(other, Symbol):
        return _internal._Div(self, other)
    if isinstance(other, Number):
        return _internal._DivScalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))