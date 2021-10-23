def list_outputs(self):
    'List all outputs in the symbol.\n\n        Returns\n        -------\n        list of str\n            List of all the outputs.\n            For most symbols, this list contains only the name of this symbol.\n            For symbol groups, this is a list with the names of all symbols\n            in the group.\n        '
    size = ctypes.c_uint()
    sarr = ctypes.POINTER(ctypes.c_char_p)()
    check_call(_LIB.MXSymbolListOutputs(self.handle, ctypes.byref(size), ctypes.byref(sarr)))
    return [py_str(sarr[i]) for i in range(size.value)]