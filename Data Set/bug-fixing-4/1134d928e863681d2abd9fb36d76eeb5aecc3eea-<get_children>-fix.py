def get_children(self):
    "Gets a new grouped symbol whose output contains\n        inputs to output nodes of the original symbol.\n\n        Example usage:\n        ----------\n        >>> x = mx.sym.Variable('x')\n        >>> y = mx.sym.Variable('y')\n        >>> z = mx.sym.Variable('z')\n        >>> a = y+z\n        >>> b = x+a\n        >>> b.get_children()\n        <Symbol Grouped>\n        >>> b.get_children().list_outputs()\n        ['x', '_plus10_output']\n        >>> b.get_children().get_children().list_outputs()\n        ['y', 'z']\n\n        Returns\n        -------\n        sgroup : Symbol or None\n            The children of the head node. If the symbol has no\n            inputs then ``None`` will be returned.\n        "
    handle = SymbolHandle()
    check_call(_LIB.MXSymbolGetChildren(self.handle, ctypes.byref(handle)))
    ret = Symbol(handle=handle)
    if (len(ret.list_outputs()) == 0):
        return None
    return ret