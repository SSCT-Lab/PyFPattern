def _infer_shape_impl(self, partial, *args, **kwargs):
    'The actual implementation for calling shape inference API.'
    if ((len(args) != 0) and (len(kwargs) != 0)):
        raise ValueError('Can only specify known argument                     shapes either by positional or kwargs way.')
    sdata = []
    indptr = [0]
    if (len(args) != 0):
        keys = None
        for (i, s) in enumerate(args):
            if (s is not None):
                if (not isinstance(s, tuple)):
                    raise TypeError(('Arguments need to be shapes (tuple), but argument %d is %s.' % (i, type(s))))
                sdata.extend(s)
            indptr.append(len(sdata))
    else:
        keys = []
        for (k, v) in kwargs.items():
            if (not isinstance(v, tuple)):
                raise TypeError(("Arguments need to be shapes (tuple), but '%s' is %s." % (k, type(v))))
            keys.append(c_str(k))
            sdata.extend(v)
            indptr.append(len(sdata))
    arg_shape_size = mx_uint()
    arg_shape_ndim = ctypes.POINTER(mx_uint)()
    arg_shape_data = ctypes.POINTER(ctypes.POINTER(mx_uint))()
    out_shape_size = mx_uint()
    out_shape_ndim = ctypes.POINTER(mx_uint)()
    out_shape_data = ctypes.POINTER(ctypes.POINTER(mx_uint))()
    aux_shape_size = mx_uint()
    aux_shape_ndim = ctypes.POINTER(mx_uint)()
    aux_shape_data = ctypes.POINTER(ctypes.POINTER(mx_uint))()
    complete = ctypes.c_int()
    if partial:
        infer_func = _LIB.MXSymbolInferShapePartial
    else:
        infer_func = _LIB.MXSymbolInferShape
    check_call(infer_func(self.handle, mx_uint((len(indptr) - 1)), c_array(ctypes.c_char_p, keys), c_array(mx_uint, indptr), c_array(mx_uint, sdata), ctypes.byref(arg_shape_size), ctypes.byref(arg_shape_ndim), ctypes.byref(arg_shape_data), ctypes.byref(out_shape_size), ctypes.byref(out_shape_ndim), ctypes.byref(out_shape_data), ctypes.byref(aux_shape_size), ctypes.byref(aux_shape_ndim), ctypes.byref(aux_shape_data), ctypes.byref(complete)))
    if (complete.value != 0):
        arg_shapes = [tuple(arg_shape_data[i][:arg_shape_ndim[i]]) for i in range(arg_shape_size.value)]
        out_shapes = [tuple(out_shape_data[i][:out_shape_ndim[i]]) for i in range(out_shape_size.value)]
        aux_shapes = [tuple(aux_shape_data[i][:aux_shape_ndim[i]]) for i in range(aux_shape_size.value)]
        return (arg_shapes, out_shapes, aux_shapes)
    else:
        return (None, None, None)