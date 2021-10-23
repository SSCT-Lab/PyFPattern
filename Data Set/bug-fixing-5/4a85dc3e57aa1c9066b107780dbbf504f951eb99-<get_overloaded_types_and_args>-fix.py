def get_overloaded_types_and_args(relevant_args):
    'Returns a list of arguments on which to call __array_function__.\n\n    Parameters\n    ----------\n    relevant_args : iterable of array-like\n        Iterable of array-like arguments to check for __array_function__\n        methods.\n\n    Returns\n    -------\n    overloaded_types : collection of types\n        Types of arguments from relevant_args with __array_function__ methods.\n    overloaded_args : list\n        Arguments from relevant_args on which to call __array_function__\n        methods, in the order in which they should be called.\n    '
    overloaded_types = []
    overloaded_args = []
    for arg in relevant_args:
        arg_type = type(arg)
        if ((arg_type not in overloaded_types) and hasattr(arg_type, '__array_function__')):
            overloaded_types.append(arg_type)
            index = len(overloaded_args)
            for (i, old_arg) in enumerate(overloaded_args):
                if issubclass(arg_type, type(old_arg)):
                    index = i
                    break
            overloaded_args.insert(index, arg)
    overloaded_args = [arg for arg in overloaded_args if (type(arg).__array_function__ is not _NDARRAY_ARRAY_FUNCTION)]
    return (overloaded_types, overloaded_args)