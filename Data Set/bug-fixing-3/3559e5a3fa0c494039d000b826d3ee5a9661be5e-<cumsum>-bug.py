def cumsum(x, axis=None, exclusive=None, reverse=None):
    locals_var = locals()
    kwargs = dict()
    for (name, val) in locals_var.items():
        if (val is not None):
            kwargs[name] = val
    return _cum_sum_(**kwargs)