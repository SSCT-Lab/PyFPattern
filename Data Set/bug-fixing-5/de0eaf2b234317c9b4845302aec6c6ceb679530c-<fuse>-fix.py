def fuse(*args, **kwargs):
    'Function fusing decorator.\n\n    It calls :func:`cupy.fuse` when CuPy is available to make fused function\n    and does nothing otherwise.\n\n    .. seealso::\n       :func:`cupy.fuse`\n\n    '
    if available:
        return cupy.fuse(*args, **kwargs)
    elif ((len(args) == 1) and (len(kwargs) == 0) and callable(args[0])):
        return args[0]
    else:
        return (lambda f: f)