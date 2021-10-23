def get_function_signature(function, method=True):
    wrapped = getattr(function, '_original_function', None)
    if (wrapped is None):
        signature = inspect.getargspec(function)
    else:
        signature = inspect.getargspec(wrapped)
    defaults = signature.defaults
    if method:
        args = signature.args[1:]
    else:
        args = signature.args
    if defaults:
        kwargs = zip(args[(- len(defaults)):], defaults)
        args = args[:(- len(defaults))]
    else:
        kwargs = []
    st = ('%s.%s(' % (clean_module_name(function.__module__), function.__name__))
    for a in args:
        st += (str(a) + ', ')
    for (a, v) in kwargs:
        if isinstance(v, str):
            v = (("'" + v) + "'")
        st += (((str(a) + '=') + str(v)) + ', ')
    if (kwargs or args):
        signature = (st[:(- 2)] + ')')
    else:
        signature = (st + ')')
    if (not method):
        signature = ((clean_module_name(function.__module__) + '.') + signature)
    return post_process_signature(signature)