def __gt__(self, other):
    'x.__gt__(y) <=> x>y '
    if isinstance(other, Symbol):
        return _internal._greater(self, other)
    if isinstance(other, numeric_types):
        return _internal._greater_scalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))