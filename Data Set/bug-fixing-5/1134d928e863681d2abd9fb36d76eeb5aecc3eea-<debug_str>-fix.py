def debug_str(self):
    'Gets a debug string.\n\n        Returns\n        -------\n        debug_str : string\n            Debug string of the symbol.\n        '
    debug_str = ctypes.c_char_p()
    check_call(_LIB.MXSymbolPrint(self.handle, ctypes.byref(debug_str)))
    return py_str(debug_str.value)