def grad(self, wrt):
    'Get the autodiff of current symbol.\n\n        This function can only be used if current symbol is a loss function.\n\n        .. note:: This function is currently not implemented.\n\n        Parameters\n        ----------\n        wrt : Array of String\n            keyword arguments of the symbol that the gradients are taken.\n\n        Returns\n        -------\n        grad : Symbol\n            A gradient Symbol with returns to be the corresponding gradients.\n        '
    handle = SymbolHandle()
    c_wrt = c_array(ctypes.c_char_p, [c_str(key) for key in wrt])
    check_call(_LIB.MXSymbolGrad(self.handle, mx_uint(len(wrt)), c_wrt, ctypes.byref(handle)))
    return Symbol(handle)