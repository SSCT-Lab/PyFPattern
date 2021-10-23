def list_auxiliary_states(self):
    'List all auxiliary states in the symbol.\n\n        Returns\n        -------\n        aux_states : list of string\n            List the names of the auxiliary states.\n\n        Notes\n        -----\n        Auxiliary states are special states of symbols that do not correspond to an argument,\n        and are not updated by gradient descent. Common examples of auxiliary states\n        include the `moving_mean` and `moving_variance` in `BatchNorm`.\n        Most operators do not have auxiliary states.\n        '
    size = ctypes.c_uint()
    sarr = ctypes.POINTER(ctypes.c_char_p)()
    check_call(_LIB.MXSymbolListAuxiliaryStates(self.handle, ctypes.byref(size), ctypes.byref(sarr)))
    return [py_str(sarr[i]) for i in range(size.value)]