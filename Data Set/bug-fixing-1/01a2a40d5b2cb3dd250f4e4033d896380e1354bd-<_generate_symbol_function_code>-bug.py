

def _generate_symbol_function_code(handle, name, func_name, signature_only=False):
    'Generate function for symbol op by handle and function name.'
    real_name = ctypes.c_char_p()
    desc = ctypes.c_char_p()
    num_args = mx_uint()
    arg_names = ctypes.POINTER(ctypes.c_char_p)()
    arg_types = ctypes.POINTER(ctypes.c_char_p)()
    arg_descs = ctypes.POINTER(ctypes.c_char_p)()
    key_var_num_args = ctypes.c_char_p()
    ret_type = ctypes.c_char_p()
    check_call(_LIB.MXSymbolGetAtomicSymbolInfo(handle, ctypes.byref(real_name), ctypes.byref(desc), ctypes.byref(num_args), ctypes.byref(arg_names), ctypes.byref(arg_types), ctypes.byref(arg_descs), ctypes.byref(key_var_num_args), ctypes.byref(ret_type)))
    narg = int(num_args.value)
    arg_names = [py_str(arg_names[i]) for i in range(narg)]
    arg_types = [py_str(arg_types[i]) for i in range(narg)]
    key_var_num_args = py_str(key_var_num_args.value)
    ret_type = (py_str(ret_type.value) if (ret_type.value is not None) else '')
    doc_str = _build_doc(name, py_str(desc.value), arg_names, arg_types, [py_str(arg_descs[i]) for i in range(narg)], key_var_num_args, ret_type)
    dtype_name = None
    arr_name = None
    ndsignature = []
    signature = []
    ndarg_names = []
    kwarg_names = []
    for i in range(narg):
        (name, atype) = (arg_names[i], arg_types[i])
        if (name == 'dtype'):
            dtype_name = name
            signature.append(('%s=_Null' % name))
        elif (atype.startswith('NDArray') or atype.startswith('Symbol')):
            assert (not arr_name), 'Op can only have one argument with variable size and it must be the last argument.'
            if atype.endswith('[]'):
                ndsignature.append(('*%s' % name))
                arr_name = name
            else:
                ndsignature.append(('%s=None' % name))
                ndarg_names.append(name)
        else:
            signature.append(('%s=_Null' % name))
            kwarg_names.append(name)
    signature.append('name=None')
    signature.append('attr=None')
    signature.append('out=None')
    signature.append('**kwargs')
    signature = (ndsignature + signature)
    code = []
    if arr_name:
        code.append(('\ndef %s(*%s, **kwargs):' % (func_name, arr_name)))
        if (not signature_only):
            code.append('\n    sym_args = []\n    for i in {}:\n        assert isinstance(i, SymbolBase), \\\n            "Positional arguments must be Symbol instances, " \\\n            "but got %s"%str(i)\n        sym_args.append(i)'.format(arr_name))
            if (dtype_name is not None):
                code.append(("\n    if '%s' in kwargs:\n        kwargs['%s'] = np.dtype(kwargs['%s']).name" % (dtype_name, dtype_name, dtype_name)))
            code.append(("\n    attr = kwargs.pop('attr', None)\n    kwargs.update(AttrScope.current.get(attr))\n    name = kwargs.pop('name', None)\n    name = NameManager.current.get(name, '%s')\n    _ = kwargs.pop('out', None)\n    keys = []\n    vals = []\n    sym_kwargs = dict()\n    for k, v in kwargs.items():\n        if isinstance(v, SymbolBase):\n            sym_kwargs[k] = v\n        else:\n            keys.append(k)\n            vals.append(v)" % func_name.lower()))
            if key_var_num_args:
                code.append(("\n    if '%s' not in kwargs:\n        keys.append('%s')\n        vals.append(len(sym_args) + len(sym_kwargs))" % (key_var_num_args, key_var_num_args)))
            code.append(('\n    return _symbol_creator(%d, sym_args, sym_kwargs, keys, vals, name)' % handle.value))
    else:
        code.append(('\ndef %s(%s):' % (func_name, ', '.join(signature))))
        if (not signature_only):
            code.append('\n    kwargs.update(AttrScope.current.get(attr))\n    sym_kwargs = dict()\n    keys = []\n    vals = []\n    for k, v in kwargs.items():\n        if isinstance(v, SymbolBase):\n            sym_kwargs[k] = v\n        else:\n            keys.append(k)\n            vals.append(v)')
            for name in ndarg_names:
                code.append('\n    if {name} is not None:\n        assert isinstance({name}, SymbolBase), \\\n            "Argument {name} must be Symbol instances, but got %s"%str({name})\n        sym_kwargs[\'{name}\'] = {name}'.format(name=name))
            for name in kwarg_names:
                code.append(("\n    if %s is not _Null:\n        keys.append('%s')\n        vals.append(%s)" % (name, name, name)))
            if (dtype_name is not None):
                code.append(("\n    if %s is not _Null:\n        keys.append('%s')\n        vals.append(np.dtype(%s).name)" % (dtype_name, dtype_name, dtype_name)))
            code.append(("\n    name = NameManager.current.get(name, '%s')\n    return _symbol_creator(%d, None, sym_kwargs, keys, vals, name)" % (func_name.lower(), handle.value)))
    if signature_only:
        code.append('\n    return (0,)')
    doc_str_lines = (_os.linesep + ''.join([(('    ' + s) if s.strip() else s) for s in 'r"""{doc_str}"""'.format(doc_str=doc_str).splitlines(True)]))
    code.insert(1, doc_str_lines)
    return (''.join(code), doc_str)
