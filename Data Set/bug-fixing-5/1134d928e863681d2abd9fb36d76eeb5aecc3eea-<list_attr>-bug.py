def list_attr(self, recursive=False):
    'Get all attributes from the symbol.\n\n        Returns\n        -------\n        ret : dict of str to str\n            A dicitonary mapping attribute keys to values.\n        '
    if recursive:
        raise DeprecationWarning('Symbol.list_attr with recursive=True has been deprecated. Please use attr_dict instead.')
    size = mx_uint()
    pairs = ctypes.POINTER(ctypes.c_char_p)()
    f_handle = _LIB.MXSymbolListAttrShallow
    check_call(f_handle(self.handle, ctypes.byref(size), ctypes.byref(pairs)))
    return {py_str(pairs[(i * 2)]): py_str(pairs[((i * 2) + 1)]) for i in range(size.value)}