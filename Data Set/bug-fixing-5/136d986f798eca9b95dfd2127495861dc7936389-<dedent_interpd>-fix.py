def dedent_interpd(func):
    "Dedent *func*'s docstring, then interpolate it with ``interpd``."
    func.__doc__ = inspect.getdoc(func)
    return interpd(func)