

def fn_args(fn):
    'Get argument names for function-like object.\n\n  Args:\n    fn: Function, or function-like object (e.g., result of `functools.partial`).\n\n  Returns:\n    `tuple` of string argument names.\n\n  Raises:\n    ValueError: if partial function has positionally bound arguments\n  '
    if isinstance(fn, functools.partial):
        args = fn_args(fn.func)
        args = [a for a in args[len(fn.args):] if (a not in (fn.keywords or []))]
    else:
        if _is_callable_object(fn):
            fn = fn.__call__
        args = tf_inspect.getfullargspec(fn).args
        if _is_bounded_method(fn):
            args.remove('self')
    return tuple(args)
