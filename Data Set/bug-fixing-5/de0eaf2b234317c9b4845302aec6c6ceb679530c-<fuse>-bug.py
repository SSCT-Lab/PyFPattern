def fuse(*args, **kwargs):
    'Function fusing decorator.\n\n    It calls :func:`cupy.fuse` when CuPy is available to make fused function\n    and does nothing otherwise.\n\n    .. seealso::\n       :func:`cupy.fuse`\n\n    '
    if available:
        return cupy.fuse(*args, **kwargs)
    else:
        return (lambda f: f)