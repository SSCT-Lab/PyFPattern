

def uniform(shape, dtype, low=None, high=None, *, random_state=None):
    if (random_state is None):
        random_state = numpy.random.RandomState()
    kind = numpy.dtype(dtype).kind
    if (kind == 'f'):
        return random_state.uniform(((- 1) if (low is None) else low), (1 if (high is None) else high), shape).astype(dtype, copy=False)
    if (kind == 'u'):
        return random_state.randint((0 if (low is None) else low), (4 if (high is None) else high), size=shape, dtype=dtype)
    if (kind == 'i'):
        return random_state.randint(((- 2) if (low is None) else low), (3 if (high is None) else high), size=shape, dtype=dtype)
    if (kind == 'b'):
        return random_state.randint((0 if (low is None) else low), (2 if (high is None) else high), size=shape, dtype=dtype)
    assert False, dtype
