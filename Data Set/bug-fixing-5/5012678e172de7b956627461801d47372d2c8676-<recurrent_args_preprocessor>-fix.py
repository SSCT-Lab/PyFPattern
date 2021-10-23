def recurrent_args_preprocessor(args, kwargs):
    converted = []
    if ('forget_bias_init' in kwargs):
        if (kwargs['forget_bias_init'] == 'one'):
            kwargs.pop('forget_bias_init')
            kwargs['unit_forget_bias'] = True
            converted.append(('forget_bias_init', 'unit_forget_bias'))
        else:
            kwargs.pop('forget_bias_init')
            warnings.warn('The `forget_bias_init` argument has been ignored. Use `unit_forget_bias=True` instead to initialize with ones.', stacklevel=3)
    if ('input_dim' in kwargs):
        input_length = kwargs.pop('input_length', None)
        input_dim = kwargs.pop('input_dim')
        input_shape = (input_length, input_dim)
        kwargs['input_shape'] = input_shape
        converted.append(('input_dim', 'input_shape'))
        warnings.warn('The `input_dim` and `input_length` arguments in recurrent layers are deprecated. Use `input_shape` instead.', stacklevel=3)
    return (args, kwargs, converted)