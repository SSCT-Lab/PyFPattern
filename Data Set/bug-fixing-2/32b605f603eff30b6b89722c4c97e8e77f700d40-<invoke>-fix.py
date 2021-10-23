

def invoke(self, method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except AttributeError:
        exc = get_exception()
        raise NetworkError(('undefined method "%s"' % method.__name__), exc=str(exc))
    except NotImplementedError:
        raise NetworkError(('method not supported "%s"' % method.__name__))
