def array_function_dispatch(dispatcher):
    'Wrap a function for dispatch with the __array_function__ protocol.'

    def decorator(func):

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            relevant_arguments = dispatcher(*args, **kwargs)
            (types, overloaded_args) = get_overloaded_types_and_args(relevant_arguments)
            if overloaded_args:
                return array_function_override(overloaded_args, new_func, types, args, kwargs)
            else:
                return func(*args, **kwargs)
        return new_func
    return decorator