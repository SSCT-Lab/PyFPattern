

def _wrapfunc(obj, method, *args, **kwds):
    bound = getattr(obj, method, None)
    if (bound is None):
        return _wrapit(obj, method, *args, **kwds)
    try:
        return bound(*args, **kwds)
    except TypeError:
        return _wrapit(obj, method, *args, **kwds)
