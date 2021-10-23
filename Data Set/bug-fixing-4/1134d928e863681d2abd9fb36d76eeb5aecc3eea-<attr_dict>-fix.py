def attr_dict(self):
    "Recursively gets all attributes from the symbol and its children.\n\n        Returns\n        -------\n        ret : dict of str to dict\n            There is a key in the returned dict for every child with non-empty attribute set.\n            For each symbol, the name of the symbol is its key in the dict\n            and the correspond value is that symbol's attribute list (itself a dictionary).\n        "
    size = mx_uint()
    pairs = ctypes.POINTER(ctypes.c_char_p)()
    f_handle = _LIB.MXSymbolListAttr
    check_call(f_handle(self.handle, ctypes.byref(size), ctypes.byref(pairs)))
    ret = {
        
    }
    for i in range(size.value):
        (name, key) = py_str(pairs[(i * 2)]).split('$')
        val = py_str(pairs[((i * 2) + 1)])
        if (name not in ret):
            ret[name] = {
                
            }
        ret[name][key] = val
    return ret