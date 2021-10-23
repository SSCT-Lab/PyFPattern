def get_children(self):
    'Get a new grouped symbol whose output contains\n        inputs to output nodes of the original symbol\n\n        Returns\n        -------\n        sgroup : Symbol or None\n            The children of the head node. If the symbol has no\n            inputs then ``None`` will be returned.\n        '
    handle = SymbolHandle()
    check_call(_LIB.MXSymbolGetChildren(self.handle, ctypes.byref(handle)))
    ret = Symbol(handle=handle)
    if (len(ret.list_outputs()) == 0):
        return None
    return ret