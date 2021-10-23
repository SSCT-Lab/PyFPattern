def Group(symbols):
    "Creates a symbol that contains a collection of other symbols, grouped together.\n\n    Example\n    -------\n    >>> a = mx.sym.Variable('a')\n    >>> b = mx.sym.Variable('b')\n    >>> mx.sym.Group([a,b])\n    <Symbol Grouped>\n\n    Parameters\n    ----------\n    symbols : list\n        List of symbols to be grouped.\n\n    Returns\n    -------\n    sym : Symbol\n        A group symbol.\n     "
    if ((not symbols) or any(((not isinstance(sym, Symbol)) for sym in symbols))):
        raise TypeError('Expected a list of symbols as input')
    handle = SymbolHandle()
    check_call(_LIB.MXSymbolCreateGroup(mx_uint(len(symbols)), c_handle_array(symbols), ctypes.byref(handle)))
    return Symbol(handle)