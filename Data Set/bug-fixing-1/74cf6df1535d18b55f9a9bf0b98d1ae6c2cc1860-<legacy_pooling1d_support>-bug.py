

def legacy_pooling1d_support(func):
    'Function wrapper to convert `MaxPooling1D` or `AvgPooling1D` constructor from Keras 1 to 2.\n\n    # Arguments\n        func: `__init__` method of `MaxPooling1D` or `AvgPooling1D`.\n\n    # Returns\n        A constructor conversion wrapper.\n    '

    @six.wraps(func)
    def wrapper(*args, **kwargs):
        if (len(args) > 2):
            raise TypeError((args[0].__name__ + ' layer can have at most one positional argument (the `pool_size` argument).'))
        if ('pool_length' in kwargs):
            if (len(args) > 1):
                raise TypeError('Got both a positional argument and keyword argument for argument `pool_size` (`pool_length` in the legacy interface).')
        elif ('pool_size' in kwargs):
            if (len(args) > 1):
                raise TypeError('Got both a positional argument and keyword argument for argument `pool_size`. ')
        conversions = [('pool_length', 'pool_size'), ('border_mode', 'padding')]
        kwargs = convert_legacy_kwargs(args[0].__name__, args[1:], kwargs, conversions)
        return func(*args, **kwargs)
    return wrapper
