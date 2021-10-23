@rewrite_axis_style_signature('mapper', [('copy', True), ('inplace', False)])
def rename_axis(self, mapper=None, **kwargs):
    '\n        Alter the name of the index or name of Index object that is the\n        columns.\n\n        Parameters\n        ----------\n        mapper : scalar, list-like, optional\n            Value to set the axis name attribute.\n        index, columns : scalar, list-like, dict-like or function, optional\n            dict-like or functions transformations to apply to\n            that axis\' values.\n\n            Use either ``mapper`` and ``axis`` to\n            specify the axis to target with ``mapper``, or ``index``\n            and/or ``columns``.\n\n            .. versionchanged:: 0.24.0\n\n        axis : int or string, default 0\n        copy : boolean, default True\n            Also copy underlying data.\n        inplace : boolean, default False\n            Modifies the object directly, instead of creating a new Series\n            or DataFrame.\n\n        Returns\n        -------\n        renamed : Series, DataFrame, or None\n            The same type as the caller or None if `inplace` is True.\n\n        Notes\n        -----\n        Prior to version 0.21.0, ``rename_axis`` could also be used to change\n        the axis *labels* by passing a mapping or scalar. This behavior is\n        deprecated and will be removed in a future version. Use ``rename``\n        instead.\n\n        ``DataFrame.rename_axis`` supports two calling conventions\n\n        * ``(index=index_mapper, columns=columns_mapper, ...)``\n        * ``(mapper, axis={\'index\', \'columns\'}, ...)``\n\n        The first calling convention will only modify the names of\n        the index and/or the names of the Index object that is the columns.\n        In this case, the parameter ``copy`` is ignored.\n\n        The second calling convention will modify the names of the\n        the corresponding index if mapper is a list or a scalar.\n        However, if mapper is dict-like or a function, it will use the\n        deprecated behavior of modifying the axis *labels*.\n\n        We *highly* recommend using keyword arguments to clarify your\n        intent.\n\n        See Also\n        --------\n        Series.rename : Alter Series index labels or name.\n        DataFrame.rename : Alter DataFrame index labels or name.\n        Index.rename : Set new names on index.\n\n        Examples\n        --------\n        **Series**\n\n        >>> s = pd.Series([1, 2, 3])\n        >>> s.rename_axis("foo")\n        foo\n        0    1\n        1    2\n        2    3\n        dtype: int64\n\n        **DataFrame**\n\n        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})\n        >>> df.rename_axis("foo")\n             A  B\n        foo\n        0    1  4\n        1    2  5\n        2    3  6\n\n        >>> df.rename_axis("bar", axis="columns")\n        bar  A  B\n        0    1  4\n        1    2  5\n        2    3  6\n\n        >>> mi = pd.MultiIndex.from_product([[\'a\', \'b\', \'c\'], [1, 2]],\n        ...                                 names=[\'let\',\'num\'])\n        >>> df = pd.DataFrame({\'x\': [i for i in range(len(mi))],\n        ...                    \'y\' : [i*10 for i in range(len(mi))]},\n        ...                    index=mi)\n        >>> df.rename_axis(index={\'num\' : \'n\'})\n               x   y\n        let n\n        a   1  0   0\n            2  1  10\n        b   1  2  20\n            2  3  30\n        c   1  4  40\n            2  5  50\n\n        >>> cdf = df.rename_axis(columns=\'col\')\n        >>> cdf\n        col      x   y\n        let num\n        a   1    0   0\n            2    1  10\n        b   1    2  20\n            2    3  30\n        c   1    4  40\n            2    5  50\n\n        >>> cdf.rename_axis(columns=str.upper)\n        COL      x   y\n        let num\n        a   1    0   0\n            2    1  10\n        b   1    2  20\n            2    3  30\n        c   1    4  40\n            2    5  50\n        '
    (axes, kwargs) = self._construct_axes_from_arguments((), kwargs)
    copy = kwargs.pop('copy', True)
    inplace = kwargs.pop('inplace', False)
    axis = kwargs.pop('axis', 0)
    if (axis is not None):
        axis = self._get_axis_number(axis)
    if kwargs:
        raise TypeError('rename_axis() got an unexpected keyword argument "{0}"'.format(list(kwargs.keys())[0]))
    inplace = validate_bool_kwarg(inplace, 'inplace')
    if (mapper is not None):
        non_mapper = (is_scalar(mapper) or (is_list_like(mapper) and (not is_dict_like(mapper))))
        if non_mapper:
            return self._set_axis_name(mapper, axis=axis, inplace=inplace)
        else:
            msg = "Using 'rename_axis' to alter labels is deprecated. Use '.rename' instead"
            warnings.warn(msg, FutureWarning, stacklevel=3)
            axis = self._get_axis_name(axis)
            d = {
                'copy': copy,
                'inplace': inplace,
            }
            d[axis] = mapper
            return self.rename(**d)
    else:
        result = (self if inplace else self.copy(deep=copy))
        for axis in lrange(self._AXIS_LEN):
            v = axes.get(self._AXIS_NAMES[axis])
            if (v is None):
                continue
            non_mapper = (is_scalar(v) or (is_list_like(v) and (not is_dict_like(v))))
            if non_mapper:
                newnames = v
            else:
                f = com._get_rename_function(v)
                curnames = self._get_axis(axis).names
                newnames = [f(name) for name in curnames]
            result._set_axis_name(newnames, axis=axis, inplace=True)
        if (not inplace):
            return result