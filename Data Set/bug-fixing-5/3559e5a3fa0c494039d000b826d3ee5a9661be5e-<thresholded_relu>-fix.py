def thresholded_relu(x, threshold=None):
    locals_var = locals().copy()
    kwargs = dict()
    for (name, val) in locals_var.items():
        if (val is not None):
            kwargs[name] = val
    return _thresholded_relu_(**kwargs)