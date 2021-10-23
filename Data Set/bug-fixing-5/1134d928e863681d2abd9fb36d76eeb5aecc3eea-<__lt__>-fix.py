def __lt__(self, other):
    'x.__lt__(y) <=> x<y\n        Scalar input is supported.\n        Broadcasting is not supported. Use `broadcast_lesser` instead. '
    if isinstance(other, Symbol):
        return _internal._lesser(self, other)
    if isinstance(other, numeric_types):
        return _internal._lesser_scalar(self, scalar=other)
    else:
        raise TypeError(('type %s not supported' % str(type(other))))