

def deprecate(*args, **kwargs):
    "\n    Issues a DeprecationWarning, adds warning to `old_name`'s\n    docstring, rebinds ``old_name.__name__`` and returns the new\n    function object.\n\n    This function may also be used as a decorator.\n\n    Parameters\n    ----------\n    func : function\n        The function to be deprecated.\n    old_name : str, optional\n        The name of the function to be deprecated. Default is None, in\n        which case the name of `func` is used.\n    new_name : str, optional\n        The new name for the function. Default is None, in which case the\n        deprecation message is that `old_name` is deprecated. If given, the\n        deprecation message is that `old_name` is deprecated and `new_name`\n        should be used instead.\n    message : str, optional\n        Additional explanation of the deprecation.  Displayed in the\n        docstring after the warning.\n\n    Returns\n    -------\n    old_func : function\n        The deprecated function.\n\n    Examples\n    --------\n    Note that ``olduint`` returns a value after printing Deprecation\n    Warning:\n\n    >>> olduint = np.deprecate(np.uint)\n    >>> olduint(6)\n    /usr/lib/python2.5/site-packages/numpy/lib/utils.py:114:\n    DeprecationWarning: uint32 is deprecated\n      warnings.warn(str1, DeprecationWarning, stacklevel=2)\n    6\n\n    "
    if args:
        fn = args[0]
        args = args[1:]
        return _Deprecate(*args, **kwargs)(fn)
    else:
        return _Deprecate(*args, **kwargs)
