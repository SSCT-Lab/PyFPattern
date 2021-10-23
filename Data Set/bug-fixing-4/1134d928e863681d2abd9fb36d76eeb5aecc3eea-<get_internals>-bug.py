def get_internals(self):
    "Get a new grouped symbol sgroup. The output of sgroup is a list of the\n        outputs of all of the internal nodes.\n\n        Consider the following code:\n        >>> a = mxnet.sym.var('a')\n        >>> b = mxnet.sym.var('b')\n        >>> c = a + b\n        >>> d = c.get_internals()\n        >>> d\n        <Symbol Grouped>\n        >>> d.list_outputs()\n        ['a', 'b', '_plus4_output']\n\n        Returns\n        -------\n        sgroup : Symbol\n            A symbol group containing all internal and leaf nodes of the computation graph\n            used to compute the symbol\n        "
    handle = SymbolHandle()
    check_call(_LIB.MXSymbolGetInternals(self.handle, ctypes.byref(handle)))
    return Symbol(handle=handle)