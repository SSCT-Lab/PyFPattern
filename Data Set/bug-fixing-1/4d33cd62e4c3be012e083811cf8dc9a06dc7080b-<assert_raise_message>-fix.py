

def assert_raise_message(exceptions, message, function, *args, **kwargs):
    'Helper function to test error messages in exceptions.\n\n    Parameters\n    ----------\n    exceptions : exception or tuple of exception\n        Name of the estimator\n\n    function : callable\n        Calable object to raise error\n\n    *args : the positional arguments to `function`.\n\n    **kw : the keyword arguments to `function`\n    '
    try:
        function(*args, **kwargs)
    except exceptions as e:
        error_message = str(e)
        if (message not in error_message):
            raise AssertionError(('Error message does not include the expected string: %r. Observed error message: %r' % (message, error_message)))
    else:
        if isinstance(exceptions, tuple):
            names = ' or '.join((e.__name__ for e in exceptions))
        else:
            names = exceptions.__name__
        raise AssertionError(('%s not raised by %s' % (names, function.__name__)))
