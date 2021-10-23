

def query(self, expr, inplace=False, **kwargs):
    "Query the columns of a frame with a boolean expression.\n\n        Parameters\n        ----------\n        expr : string\n            The query string to evaluate.  You can refer to variables\n            in the environment by prefixing them with an '@' character like\n            ``@a + b``.\n        inplace : bool\n            Whether the query should modify the data in place or return\n            a modified copy\n\n            .. versionadded:: 0.18.0\n\n        kwargs : dict\n            See the documentation for :func:`pandas.eval` for complete details\n            on the keyword arguments accepted by :meth:`DataFrame.query`.\n\n        Returns\n        -------\n        q : DataFrame\n\n        Notes\n        -----\n        The result of the evaluation of this expression is first passed to\n        :attr:`DataFrame.loc` and if that fails because of a\n        multidimensional key (e.g., a DataFrame) then the result will be passed\n        to :meth:`DataFrame.__getitem__`.\n\n        This method uses the top-level :func:`pandas.eval` function to\n        evaluate the passed query.\n\n        The :meth:`~pandas.DataFrame.query` method uses a slightly\n        modified Python syntax by default. For example, the ``&`` and ``|``\n        (bitwise) operators have the precedence of their boolean cousins,\n        :keyword:`and` and :keyword:`or`. This *is* syntactically valid Python,\n        however the semantics are different.\n\n        You can change the semantics of the expression by passing the keyword\n        argument ``parser='python'``. This enforces the same semantics as\n        evaluation in Python space. Likewise, you can pass ``engine='python'``\n        to evaluate an expression using Python itself as a backend. This is not\n        recommended as it is inefficient compared to using ``numexpr`` as the\n        engine.\n\n        The :attr:`DataFrame.index` and\n        :attr:`DataFrame.columns` attributes of the\n        :class:`~pandas.DataFrame` instance are placed in the query namespace\n        by default, which allows you to treat both the index and columns of the\n        frame as a column in the frame.\n        The identifier ``index`` is used for the frame index; you can also\n        use the name of the index to identify it in a query. Please note that\n        Python keywords may not be used as identifiers.\n\n        For further details and examples see the ``query`` documentation in\n        :ref:`indexing <indexing.query>`.\n\n        See Also\n        --------\n        pandas.eval\n        DataFrame.eval\n\n        Examples\n        --------\n        >>> import numpy as np\n        >>> import pandas as pd\n        >>> df = pd.DataFrame(np.random.randn(10, 2), columns=list('ab'))\n        >>> df.query('a > b')\n        >>> df[df.a > df.b]  # same result as the previous expression\n        "
    inplace = validate_bool_kwarg(inplace, 'inplace')
    if (not isinstance(expr, compat.string_types)):
        msg = 'expr must be a string to be evaluated, {0} given'
        raise ValueError(msg.format(type(expr)))
    kwargs['level'] = (kwargs.pop('level', 0) + 1)
    kwargs['target'] = None
    res = self.eval(expr, **kwargs)
    try:
        new_data = self.loc[res]
    except ValueError:
        new_data = self[res]
    if inplace:
        self._update_inplace(new_data)
    else:
        return new_data
