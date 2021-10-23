def attr(self, key):
    'Get attribute string from the symbol. This function only works for non-grouped symbols.\n\n        Parameters\n        ----------\n        key : str\n            The key corresponding to the desired attribute.\n\n        Returns\n        -------\n        value : str\n            The desired attribute value, returns None if attribute does not exist.\n        '
    ret = ctypes.c_char_p()
    success = ctypes.c_int()
    check_call(_LIB.MXSymbolGetAttr(self.handle, c_str(key), ctypes.byref(ret), ctypes.byref(success)))
    if (success.value != 0):
        return py_str(ret.value)
    else:
        return None