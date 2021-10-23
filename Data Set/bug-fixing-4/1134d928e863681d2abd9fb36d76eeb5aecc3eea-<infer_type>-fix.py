def infer_type(self, *args, **kwargs):
    "Infers the type of all arguments and all outputs, given the known types\n        for some arguments.\n\n        This function takes the known types of some arguments in either positional way\n        or keyword argument way as input. It returns a tuple of `None` values\n        if there is not enough information to deduce the missing types.\n\n        Inconsistencies in the known types will cause an error to be raised.\n\n        Example usage:\n        ----------\n        >>> a = mx.sym.var('a')\n        >>> b = mx.sym.var('b')\n        >>> c = a + b\n        >>> arg_types, out_types, aux_types = c.infer_type(a='float32')\n        >>> arg_types\n        [<type 'numpy.float32'>, <type 'numpy.float32'>]\n        >>> out_types\n        [<type 'numpy.float32'>]\n        >>> aux_types\n        []\n\n        Parameters\n        ----------\n        *args :\n            Type of known arguments in a positional way.\n            Unknown type can be marked as None.\n\n        **kwargs :\n            Keyword arguments of known types.\n\n        Returns\n        -------\n        arg_types : list of numpy.dtype or None\n            List of argument types.\n            The order is same as the order of list_arguments().\n        out_types : list of numpy.dtype or None\n            List of output types.\n            The order is same as the order of list_outputs().\n        aux_types : list of numpy.dtype or None\n            List of auxiliary state types.\n            The order is same as the order of list_auxiliary_states().\n        "
    if ((len(args) != 0) and (len(kwargs) != 0)):
        raise ValueError('Can only specify known argument                     types either by positional or kwargs way.')
    sdata = []
    if (len(args) != 0):
        keys = None
        for s in args:
            if (s is not None):
                s = _numpy.dtype(s).type
                if (s not in _DTYPE_NP_TO_MX):
                    raise TypeError(('Argument need to be one of ' + str(_DTYPE_NP_TO_MX)))
                sdata.append(_DTYPE_NP_TO_MX[s])
            else:
                sdata.append((- 1))
    else:
        keys = []
        for (k, v) in kwargs.items():
            v = _numpy.dtype(v).type
            if (v in _DTYPE_NP_TO_MX):
                keys.append(c_str(k))
                sdata.append(_DTYPE_NP_TO_MX[v])
    arg_type_size = mx_uint()
    arg_type_data = ctypes.POINTER(ctypes.c_int)()
    out_type_size = mx_uint()
    out_type_data = ctypes.POINTER(ctypes.c_int)()
    aux_type_size = mx_uint()
    aux_type_data = ctypes.POINTER(ctypes.c_int)()
    complete = ctypes.c_int()
    check_call(_LIB.MXSymbolInferType(self.handle, mx_uint(len(sdata)), c_array(ctypes.c_char_p, keys), c_array(ctypes.c_int, sdata), ctypes.byref(arg_type_size), ctypes.byref(arg_type_data), ctypes.byref(out_type_size), ctypes.byref(out_type_data), ctypes.byref(aux_type_size), ctypes.byref(aux_type_data), ctypes.byref(complete)))
    if (complete.value != 0):
        arg_types = [_DTYPE_MX_TO_NP[arg_type_data[i]] for i in range(arg_type_size.value)]
        out_types = [_DTYPE_MX_TO_NP[out_type_data[i]] for i in range(out_type_size.value)]
        aux_types = [_DTYPE_MX_TO_NP[aux_type_data[i]] for i in range(aux_type_size.value)]
        return (arg_types, out_types, aux_types)
    else:
        return (None, None, None)