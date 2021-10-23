@set_module('numpy')
def isscalar(element):
    "\n    Returns True if the type of `element` is a scalar type.\n\n    Parameters\n    ----------\n    element : any\n        Input argument, can be of any type and shape.\n\n    Returns\n    -------\n    val : bool\n        True if `element` is a scalar type, False if it is not.\n\n    See Also\n    --------\n    ndim : Get the number of dimensions of an array\n\n    Notes\n    -----\n    If you need a stricter way to identify a *numerical* scalar, use\n    ``isinstance(x, numbers.Number)``, as that returns ``False`` for most\n    non-numerical elements such as strings.\n\n    In most cases ``np.ndim(x) == 0`` should be used instead of this function,\n    as that will also return true for 0d arrays. This is how numpy overloads\n    functions in the style of the ``dx`` arguments to `gradient` and the ``bins``\n    argument to `histogram`. Some key differences:\n\n    +--------------------------------------+---------------+-------------------+\n    | x                                    |``isscalar(x)``|``np.ndim(x) == 0``|\n    +======================================+===============+===================+\n    | PEP 3141 numeric objects (including  | ``True``      | ``True``          |\n    | builtins)                            |               |                   |\n    +--------------------------------------+---------------+-------------------+\n    | builtin string and buffer objects    | ``True``      | ``True``          |\n    +--------------------------------------+---------------+-------------------+\n    | other builtin objects, like          | ``False``     | ``True``          |\n    | `pathlib.Path`, `Exception`,         |               |                   |\n    | the result of `re.compile`           |               |                   |\n    +--------------------------------------+---------------+-------------------+\n    | third-party objects like             | ``False``     | ``True``          |\n    | `matplotlib.figure.Figure`           |               |                   |\n    +--------------------------------------+---------------+-------------------+\n    | zero-dimensional numpy arrays        | ``False``     | ``True``          |\n    +--------------------------------------+---------------+-------------------+\n    | other numpy arrays                   | ``False``     | ``False``         |\n    +--------------------------------------+---------------+-------------------+\n    | `list`, `tuple`, and other sequence  | ``False``     | ``False``         |\n    | objects                              |               |                   |\n    +--------------------------------------+---------------+-------------------+\n\n    Examples\n    --------\n    >>> np.isscalar(3.1)\n    True\n    >>> np.isscalar(np.array(3.1))\n    False\n    >>> np.isscalar([3.1])\n    False\n    >>> np.isscalar(False)\n    True\n    >>> np.isscalar('numpy')\n    True\n\n    NumPy supports PEP 3141 numbers:\n\n    >>> from fractions import Fraction\n    >>> np.isscalar(Fraction(5, 17))\n    True\n    >>> from numbers import Number\n    >>> np.isscalar(Number())\n    True\n\n    "
    return (isinstance(element, generic) or (type(element) in ScalarType) or isinstance(element, numbers.Number))