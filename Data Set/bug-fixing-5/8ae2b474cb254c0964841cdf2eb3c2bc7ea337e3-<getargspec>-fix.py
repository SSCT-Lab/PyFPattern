def getargspec(func):
    if PY2:
        return inspect.getargspec(func)
    sig = inspect.signature(func)
    args = [p.name for p in sig.parameters.values() if (p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    varargs = [p.name for p in sig.parameters.values() if (p.kind == inspect.Parameter.VAR_POSITIONAL)]
    varargs = (varargs[0] if varargs else None)
    varkw = [p.name for p in sig.parameters.values() if (p.kind == inspect.Parameter.VAR_KEYWORD)]
    varkw = (varkw[0] if varkw else None)
    defaults = (tuple((p.default for p in sig.parameters.values() if ((p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD) and (p.default is not p.empty)))) or None)
    return ArgSpec(args, varargs, varkw, defaults)