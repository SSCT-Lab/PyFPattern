def __le__(self, other):
    'x.__le__(y) <=> x<=y '
    if isinstance(other, Symbol):
        return _internal._lesser_equal(self, other)
    if isinstance(other, numeric_types):
        return _internal._lesser_equal_scalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))