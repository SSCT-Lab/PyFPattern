def convlstm2d_args_preprocessor(args, kwargs):
    converted = []
    if ('forget_bias_init' in kwargs):
        value = kwargs.pop('forget_bias_init')
        if (value == 'one'):
            kwargs['unit_forget_bias'] = True
            converted.append(('forget_bias_init', 'unit_forget_bias'))
        else:
            warnings.warn('The `forget_bias_init` argument has been ignored. Use `unit_forget_bias=True` instead to initialize with ones.', stacklevel=3)
    (args, kwargs, _converted) = conv2d_args_preprocessor(args, kwargs)
    return (args, kwargs, (converted + _converted))