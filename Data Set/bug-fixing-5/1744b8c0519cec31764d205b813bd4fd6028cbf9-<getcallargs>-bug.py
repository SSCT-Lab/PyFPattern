def getcallargs(func, *positional, **named):
    "TFDecorator-aware replacement for inspect.getcallargs.\n\n  Args:\n    func: A callable, possibly decorated\n    *positional: The positional arguments that would be passed to `func`.\n    **named: The named argument dictionary that would be passed to `func`.\n\n  Returns:\n    A dictionary mapping `func`'s named arguments to the values they would\n    receive if `func(*positional, **named)` were called.\n\n  `getcallargs` will use the argspec from the outermost decorator that provides\n  it. If no attached decorators modify argspec, the final unwrapped target's\n  argspec will be used.\n  "
    argspec = getargspec(func)
    call_args = named.copy()
    this = (getattr(func, 'im_self', None) or getattr(func, '__self__', None))
    if (ismethod(func) and this):
        positional = ((this,) + positional)
    remaining_positionals = [arg for arg in argspec.args if (arg not in call_args)]
    call_args.update(dict(zip(remaining_positionals, positional)))
    default_count = (0 if (not argspec.defaults) else len(argspec.defaults))
    if default_count:
        for (arg, value) in zip(argspec.args[(- default_count):], argspec.defaults):
            if (arg not in call_args):
                call_args[arg] = value
    return call_args