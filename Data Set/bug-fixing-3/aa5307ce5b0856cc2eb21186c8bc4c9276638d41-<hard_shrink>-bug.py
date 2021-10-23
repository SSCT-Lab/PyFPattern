def hard_shrink(x, threshold=None):
    locals_var = locals().keys()
    kwargs = dict()
    for name in locals_var:
        val = locals()[name]
        if (val is not None):
            kwargs[name] = val
    return _hard_shrink_(**kwargs)