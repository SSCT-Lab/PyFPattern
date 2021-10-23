def array_function_dispatch(dispatcher, module=None, verify=True, docs_from_dispatcher=False):
    "Decorator for adding dispatch with the __array_function__ protocol.\n\n    See NEP-18 for example usage.\n\n    Parameters\n    ----------\n    dispatcher : callable\n        Function that when called like ``dispatcher(*args, **kwargs)`` with\n        arguments from the NumPy function call returns an iterable of\n        array-like arguments to check for ``__array_function__``.\n    module : str, optional\n        __module__ attribute to set on new function, e.g., ``module='numpy'``.\n        By default, module is copied from the decorated function.\n    verify : bool, optional\n        If True, verify the that the signature of the dispatcher and decorated\n        function signatures match exactly: all required and optional arguments\n        should appear in order with the same names, but the default values for\n        all optional arguments should be ``None``. Only disable verification\n        if the dispatcher's signature needs to deviate for some particular\n        reason, e.g., because the function has a signature like\n        ``func(*args, **kwargs)``.\n    docs_from_dispatcher : bool, optional\n        If True, copy docs from the dispatcher function onto the dispatched\n        function, rather than from the implementation. This is useful for\n        functions defined in C, which otherwise don't have docstrings.\n\n    Returns\n    -------\n    Function suitable for decorating the implementation of a NumPy function.\n    "

    def decorator(implementation):
        if verify:
            verify_matching_signatures(implementation, dispatcher)
        if docs_from_dispatcher:
            add_docstring(implementation, dispatcher.__doc__)
        source = textwrap.dedent('\n        @functools.wraps(implementation)\n        def {name}(*args, **kwargs):\n            relevant_args = dispatcher(*args, **kwargs)\n            return implement_array_function(\n                implementation, {name}, relevant_args, args, kwargs)\n        ').format(name=implementation.__name__)
        source_object = compile(source, filename='<__array_function__ internals>', mode='exec')
        scope = {
            'implementation': implementation,
            'dispatcher': dispatcher,
            'functools': functools,
            'implement_array_function': implement_array_function,
        }
        exec(source_object, scope)
        public_api = scope[implementation.__name__]
        if (module is not None):
            public_api.__module__ = module
        return public_api
    return decorator