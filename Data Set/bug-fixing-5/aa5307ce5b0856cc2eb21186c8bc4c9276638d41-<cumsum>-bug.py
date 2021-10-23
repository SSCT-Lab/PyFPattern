def cumsum(x, axis=None, exclusive=None, reverse=None):
    locals_var = locals().keys()
    kwargs = dict()
    for name in locals_var:
        val = locals()[name]
        if (val is not None):
            kwargs[name] = val
    return _cum_sum_(**kwargs)