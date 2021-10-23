def _wrap(fmt, func, level=logging.DEBUG, always=True):
    '\n    return a callable function that wraps func and reports its\n    output through logger\n\n    if always is True, the report will occur on every function\n    call; otherwise only on the first time the function is called\n    '
    assert callable(func)

    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if (always or (not wrapper._spoke)):
            _log.log(level, (fmt % ret))
            spoke = True
            if (not wrapper._spoke):
                wrapper._spoke = spoke
        return ret
    wrapper._spoke = False
    wrapper.__doc__ = func.__doc__
    return wrapper