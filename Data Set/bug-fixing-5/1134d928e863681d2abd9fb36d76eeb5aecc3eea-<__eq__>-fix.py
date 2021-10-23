def __eq__(self, other):
    'x.__eq__(y) <=> x==y\n        Scalar input is supported.\n        Broadcasting is not supported. Use `broadcast_equal` instead. '
    if isinstance(other, Symbol):
        return _internal._equal(self, other)
    if isinstance(other, numeric_types):
        return _internal._equal_scalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))