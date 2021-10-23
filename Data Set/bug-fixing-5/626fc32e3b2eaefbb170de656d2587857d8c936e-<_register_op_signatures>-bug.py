def _register_op_signatures():
    if ((sys.version_info.major < 3) or (sys.version_info.minor < 5)):
        warnings.warn('Some mxnet.numpy operator signatures may not be displayed consistently with their counterparts in the official NumPy package due to too-low Python version {}. Python >= 3.5 is required to make the signatures display correctly.'.format(str(sys.version)))
        return
    import inspect
    for op_name in dir(_numpy_op_doc):
        op = _get_builtin_op(op_name)
        if (op is not None):
            op.__signature__ = inspect.signature(getattr(_numpy_op_doc, op_name))