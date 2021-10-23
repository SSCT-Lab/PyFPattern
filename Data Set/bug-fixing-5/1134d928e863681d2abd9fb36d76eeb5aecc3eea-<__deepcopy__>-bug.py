def __deepcopy__(self, _):
    handle = SymbolHandle()
    check_call(_LIB.MXSymbolCopy(self.handle, ctypes.byref(handle)))
    return Symbol(handle)