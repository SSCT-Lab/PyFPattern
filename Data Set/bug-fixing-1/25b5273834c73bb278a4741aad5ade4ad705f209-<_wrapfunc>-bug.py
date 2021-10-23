

def _wrapfunc(obj, method, *args, **kwds):
    try:
        return getattr(obj, method)(*args, **kwds)
    except (AttributeError, TypeError):
        return _wrapit(obj, method, *args, **kwds)
