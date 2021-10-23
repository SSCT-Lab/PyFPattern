def __deepcopy__(self, _):
    "Returns a deep copy of the input object.\n\n        This function returns a deep copy of the input object including the current state\n        of all its parameters such as weights, biases, etc.\n\n        Any changes made to the deep copy do not reflect in the original object.\n\n        Example usage:\n        ----------\n        >>> import copy\n        >>> data = mx.sym.Variable('data')\n        >>> data_1 = copy.deepcopy(data)\n        >>> data_1 = 2*data\n        >>> data_1.tojson()\n        >>> data_1 is data    # Data got modified\n        False\n        "
    handle = SymbolHandle()
    check_call(_LIB.MXSymbolCopy(self.handle, ctypes.byref(handle)))
    return Symbol(handle)