

def legacy_dense_support(func):
    'Function wrapper to convert the `Dense` constructor from Keras 1 to 2.\n\n    # Arguments\n        func: `__init__` method of `Dense`.\n\n    # Returns\n        A constructor conversion wrapper.\n    '

    @six.wraps(func)
    def wrapper(*args, **kwargs):
        if (len(args) > 2):
            raise TypeError('The `Dense` layer can have at most one positional argument (the `units` argument).')
        if ('output_dim' in kwargs):
            if (len(args) > 1):
                raise TypeError('Got both a positional argument and keyword argument for argument `units` (`output_dim` in the legacy interface).')
            if ('units' in kwargs):
                raise_duplicate_arg_error('output_dim', 'units')
            output_dim = kwargs.pop('output_dim')
            args = (args[0], output_dim)
        conversions = [('init', 'kernel_initializer'), ('W_regularizer', 'kernel_regularizer'), ('b_regularizer', 'bias_regularizer'), ('W_constraint', 'kernel_constraint'), ('b_constraint', 'bias_constraint'), ('bias', 'use_bias')]
        kwargs = convert_legacy_kwargs('Dense', args, kwargs, conversions)
        return func(*args, **kwargs)
    return wrapper
