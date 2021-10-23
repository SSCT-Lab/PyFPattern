def get_overloaded_types_and_args(relevant_args):
    'Returns a list of arguments on which to call __array_function__.\n\n    __array_function__ implementations should be called in order on the return\n    values from this function.\n    '
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