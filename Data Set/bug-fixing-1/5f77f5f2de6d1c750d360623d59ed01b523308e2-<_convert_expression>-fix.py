

def _convert_expression(expr):
    "\n    Convert an object to an expression.\n\n    This function converts an object to an expression (a unicode string) and\n    checks to make sure it isn't empty after conversion. This is used to\n    convert operators to their string representation for recursive calls to\n    :func:`~pandas.eval`.\n\n    Parameters\n    ----------\n    expr : object\n        The object to be converted to a string.\n\n    Returns\n    -------\n    s : unicode\n        The string representation of an object.\n\n    Raises\n    ------\n    ValueError\n      * If the expression is empty.\n    "
    s = pprint_thing(expr)
    _check_expression(s)
    return s
