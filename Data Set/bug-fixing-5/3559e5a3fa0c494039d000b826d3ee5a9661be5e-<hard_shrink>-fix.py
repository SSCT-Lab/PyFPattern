def hard_shrink(x, threshold=None):
    locals_var = locals().copy()
    kwargs = dict()
    for (name, val) in locals_var.items():
        if (val is not None):
            kwargs[name] = val
    return _hard_shrink_(**kwargs)