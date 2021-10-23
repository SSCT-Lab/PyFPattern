

def _check_grad_type(func, x, gx):
    if ((x.data is None) or (gx is None)):
        return
    if (not chainer.is_arrays_compatible((gx, x.data))):
        msg = ('Type of data and grad mismatch\ngrad: %s != data: %s' % (type(gx), type(x.data)))
        typ = TypeError
    elif (gx.dtype != x.data.dtype):
        msg = ('Dtype of data and grad mismatch\ngrad: %s != data: %s' % (gx.dtype, x.data.dtype))
        typ = TypeError
    elif (gx.shape != x.data.shape):
        msg = ('Shape of data and grad mismatch\ngrad: %s != data: %s' % (gx.shape, x.data.shape))
        typ = ValueError
    else:
        return
    detail = ''
    if func:
        detail = 'Function `{0}` ({1}) has a bug.\n'.format(type(func)._impl_name, func.label)
        stack = func.stack
        if stack:
            detail += 'Stacktrace of the function is below:\n'
            for line in traceback.format_list(func.stack):
                detail += line
        detail += '\nPlease report this error to the issue tracker with the stack trace,\nthe information of your environment, and your script:\nhttps://github.com/chainer/chainer/issues/new.\n'.format(type(func).__name__, func.label)
    raise typ((detail + msg))
