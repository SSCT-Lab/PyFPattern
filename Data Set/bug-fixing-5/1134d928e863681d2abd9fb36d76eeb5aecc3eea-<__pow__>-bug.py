def __pow__(self, other):
    'x.__pow__(y) <=> x**y '
    if isinstance(other, Symbol):
        return _internal._Power(self, other)
    if isinstance(other, Number):
        return _internal._PowerScalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))