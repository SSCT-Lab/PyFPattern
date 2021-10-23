def array_function_dispatch(dispatcher):
    'Decorator for adding dispatch with the __array_function__ protocol.'

    def decorator(implementation):

        @functools.wraps(implementation)
        def public_api(*args, **kwargs):
            relevant_args = dispatcher(*args, **kwargs)
            return array_function_implementation_or_override(implementation, public_api, relevant_args, args, kwargs)
        return public_api
    return decorator