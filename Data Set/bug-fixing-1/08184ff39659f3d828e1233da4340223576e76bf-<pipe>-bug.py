

def pipe(obj, func, *args, **kwargs):
    '\n    Apply a function ``func`` to object ``obj`` either by passing obj as the\n    first argument to the function or, in the case that the func is a tuple,\n    interpret the first element of the tuple as a function and pass the obj to\n    that function as a keyword argument whose key is the value of the second\n    element of the tuple.\n\n    Parameters\n    ----------\n    func : callable or tuple of (callable, string)\n        Function to apply to this object or, alternatively, a\n        ``(callable, data_keyword)`` tuple where ``data_keyword`` is a\n        string indicating the keyword of `callable`` that expects the\n        object.\n    args : iterable, optional\n        positional arguments passed into ``func``.\n    kwargs : dict, optional\n        a dictionary of keyword arguments passed into ``func``.\n\n    Returns\n    -------\n    object : the return type of ``func``.\n    '
    if isinstance(func, tuple):
        (func, target) = func
        if (target in kwargs):
            msg = ('%s is both the pipe target and a keyword argument' % target)
            raise ValueError(msg)
        kwargs[target] = obj
        return func(*args, **kwargs)
    else:
        return func(obj, *args, **kwargs)
