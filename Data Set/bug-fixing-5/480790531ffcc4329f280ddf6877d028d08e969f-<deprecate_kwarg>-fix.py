def deprecate_kwarg(old_arg_name, new_arg_name, mapping=None, stacklevel=2):
    '\n    Decorator to deprecate a keyword argument of a function.\n\n    Parameters\n    ----------\n    old_arg_name : str\n        Name of argument in function to deprecate\n    new_arg_name : str or None\n        Name of preferred argument in function. Use None to raise warning that\n        ``old_arg_name`` keyword is deprecated.\n    mapping : dict or callable\n        If mapping is present, use it to translate old arguments to\n        new arguments. A callable must do its own value checking;\n        values not found in a dict will be forwarded unchanged.\n\n    Examples\n    --------\n    The following deprecates \'cols\', using \'columns\' instead\n\n    >>> @deprecate_kwarg(old_arg_name=\'cols\', new_arg_name=\'columns\')\n    ... def f(columns=\'\'):\n    ...     print(columns)\n    ...\n    >>> f(columns=\'should work ok\')\n    should work ok\n\n    >>> f(cols=\'should raise warning\')\n    FutureWarning: cols is deprecated, use columns instead\n      warnings.warn(msg, FutureWarning)\n    should raise warning\n\n    >>> f(cols=\'should error\', columns="can\'t pass do both")\n    TypeError: Can only specify \'cols\' or \'columns\', not both\n\n    >>> @deprecate_kwarg(\'old\', \'new\', {\'yes\': True, \'no\': False})\n    ... def f(new=False):\n    ...     print(\'yes!\' if new else \'no!\')\n    ...\n    >>> f(old=\'yes\')\n    FutureWarning: old=\'yes\' is deprecated, use new=True instead\n      warnings.warn(msg, FutureWarning)\n    yes!\n\n\n    To raise a warning that a keyword will be removed entirely in the future\n\n    >>> @deprecate_kwarg(old_arg_name=\'cols\', new_arg_name=None)\n    ... def f(cols=\'\', another_param=\'\'):\n    ...     print(cols)\n    ...\n    >>> f(cols=\'should raise warning\')\n    FutureWarning: the \'cols\' keyword is deprecated and will be removed in a\n    future version please takes steps to stop use of \'cols\'\n    should raise warning\n    >>> f(another_param=\'should not raise warning\')\n    should not raise warning\n\n    >>> f(cols=\'should raise warning\', another_param=\'\')\n    FutureWarning: the \'cols\' keyword is deprecated and will be removed in a\n    future version please takes steps to stop use of \'cols\'\n    should raise warning\n    '
    if ((mapping is not None) and (not hasattr(mapping, 'get')) and (not callable(mapping))):
        raise TypeError('mapping from old to new argument values must be dict or callable!')

    def _deprecate_kwarg(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            old_arg_value = kwargs.pop(old_arg_name, None)
            if ((new_arg_name is None) and (old_arg_value is not None)):
                msg = "the '{old_name}' keyword is deprecated and will be removed in a future version. Please take steps to stop the use of '{old_name}'".format(old_name=old_arg_name)
                warnings.warn(msg, FutureWarning, stacklevel=stacklevel)
                kwargs[old_arg_name] = old_arg_value
                return func(*args, **kwargs)
            if (old_arg_value is not None):
                if (mapping is not None):
                    if hasattr(mapping, 'get'):
                        new_arg_value = mapping.get(old_arg_value, old_arg_value)
                    else:
                        new_arg_value = mapping(old_arg_value)
                    msg = 'the {old_name}={old_val!r} keyword is deprecated, use {new_name}={new_val!r} instead'.format(old_name=old_arg_name, old_val=old_arg_value, new_name=new_arg_name, new_val=new_arg_value)
                else:
                    new_arg_value = old_arg_value
                    msg = "the '{old_name}' keyword is deprecated, use '{new_name}' instead".format(old_name=old_arg_name, new_name=new_arg_name)
                warnings.warn(msg, FutureWarning, stacklevel=stacklevel)
                if (kwargs.get(new_arg_name, None) is not None):
                    msg = "Can only specify '{old_name}' or '{new_name}', not both".format(old_name=old_arg_name, new_name=new_arg_name)
                    raise TypeError(msg)
                else:
                    kwargs[new_arg_name] = new_arg_value
            return func(*args, **kwargs)
        return wrapper
    return _deprecate_kwarg