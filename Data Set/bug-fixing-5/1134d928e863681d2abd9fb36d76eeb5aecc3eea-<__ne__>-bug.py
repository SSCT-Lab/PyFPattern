def __ne__(self, other):
    'x.__ne__(y) <=> x!=y '
    if isinstance(other, Symbol):
        return _internal._not_equal(self, other)
    if isinstance(other, numeric_types):
        return _internal._not_equal_scalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))