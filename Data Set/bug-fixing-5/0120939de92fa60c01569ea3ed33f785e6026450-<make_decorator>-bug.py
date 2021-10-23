def make_decorator(target, decorator_func, decorator_name=None, decorator_doc='', decorator_argspec=None):
    'Make a decorator from a wrapper and a target.\n\n  Args:\n    target: The final callable to be wrapped.\n    decorator_func: The wrapper function.\n    decorator_name: The name of the decorator. If `None`, the name of the\n      function calling make_decorator.\n    decorator_doc: Documentation specific to this application of\n      `decorator_func` to `target`.\n    decorator_argspec: The new callable signature of this decorator.\n\n  Returns:\n    The `decorator_func` argument with new metadata attached.\n  '
    if (decorator_name is None):
        prev_frame = _inspect.currentframe().f_back
        decorator_name = _inspect.getframeinfo(prev_frame)[2]
    decorator = TFDecorator(decorator_name, target, decorator_doc, decorator_argspec)
    setattr(decorator_func, '_tf_decorator', decorator)
    decorator_func.__name__ = target.__name__
    decorator_func.__module__ = target.__module__
    decorator_func.__doc__ = decorator.__doc__
    decorator_func.__wrapped__ = target
    return decorator_func