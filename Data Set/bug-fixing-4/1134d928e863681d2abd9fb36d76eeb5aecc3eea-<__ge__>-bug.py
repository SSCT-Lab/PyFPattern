def __ge__(self, other):
    'x.__ge__(y) <=> x>=y '
    if isinstance(other, Symbol):
        return _internal._greater_equal(self, other)
    if isinstance(other, numeric_types):
        return _internal._greater_equal_scalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))