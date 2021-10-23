@contextlib.contextmanager
def assert_warns(expected):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        (yield)
    if any((isinstance(m.message, expected) for m in w)):
        return
    try:
        exc_name = expected.__name__
    except AttributeError:
        exc_name = str(expected)
    raise AssertionError(('%s not triggerred' % exc_name))