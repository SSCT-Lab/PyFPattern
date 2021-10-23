@rewrite_axis_style_signature('mapper', [('copy', True), ('inplace', False)])
def rename_axis(self, mapper=None, **kwargs):
    '\n        Set the name of the axis for the index or columns.\n\n        Parameters\n        ----------\n        mapper : scalar, list-like, optional\n            Value to set the axis name attribute.\n        index, columns : scalar, list-like, dict-like or function, optional\n            A scalar, list-like, dict-like or functions transformations to\n            apply to that axis\' values.\n\n            Use either ``mapper`` and ``axis`` to\n            specify the axis to target with ``mapper``, or ``index``\n            and/or ``columns``.\n\n            .. versionchanged:: 0.24.0\n\n        axis : {0 or \'index\', 1 or \'columns\'}, default 0\n            The axis to rename.\n        copy : bool, default True\n            Also copy underlying data.\n        inplace : bool, default False\n            Modifies the object directly, instead of creating a new Series\n            or DataFrame.\n\n        Returns\n        -------\n        Series, DataFrame, or None\n            The same type as the caller or None if `inplace` is True.\n\n        See Also\n        --------\n        Series.rename : Alter Series index labels or name.\n        DataFrame.rename : Alter DataFrame index labels or name.\n        Index.rename : Set new names on index.\n\n        Notes\n        -----\n        Prior to version 0.21.0, ``rename_axis`` could also be used to change\n        the axis *labels* by passing a mapping or scalar. This behavior is\n        deprecated and will be removed in a future version. Use ``rename``\n        instead.\n\n        ``DataFrame.rename_axis`` supports two calling conventions\n\n        * ``(index=index_mapper, columns=columns_mapper, ...)``\n        * ``(mapper, axis={\'index\', \'columns\'}, ...)``\n\n        The first calling convention will only modify the names of\n        the index and/or the names of the Index object that is the columns.\n        In this case, the parameter ``copy`` is ignored.\n\n        The second calling convention will modify the names of the\n        the corresponding index if mapper is a list or a scalar.\n        However, if mapper is dict-like or a function, it will use the\n        deprecated behavior of modifying the axis *labels*.\n\n        We *highly* recommend using keyword arguments to clarify your\n        intent.\n\n        Examples\n        --------\n        **Series**\n\n        >>> s = pd.Series(["dog", "cat", "monkey"])\n        >>> s\n        0       dog\n        1       cat\n        2    monkey\n        dtype: object\n        >>> s.rename_axis("animal")\n        animal\n        0    dog\n        1    cat\n        2    monkey\n        dtype: object\n\n        **DataFrame**\n\n        >>> df = pd.DataFrame({"num_legs": [4, 4, 2],\n        ...                    "num_arms": [0, 0, 2]},\n        ...                   ["dog", "cat", "monkey"])\n        >>> df\n                num_legs  num_arms\n        dog            4         0\n        cat            4         0\n        monkey         2         2\n        >>> df = df.rename_axis("animal")\n        >>> df\n                num_legs  num_arms\n        animal\n        dog            4         0\n        cat            4         0\n        monkey         2         2\n        >>> df = df.rename_axis("limbs", axis="columns")\n        >>> df\n        limbs   num_legs  num_arms\n        animal\n        dog            4         0\n        cat            4         0\n        monkey         2         2\n\n        **MultiIndex**\n\n        >>> df.index = pd.MultiIndex.from_product([[\'mammal\'],\n        ...                                        [\'dog\', \'cat\', \'monkey\']],\n        ...                                       names=[\'type\', \'name\'])\n        >>> df\n        limbs          num_legs  num_arms\n        type   name\n        mammal dog            4         0\n               cat            4         0\n               monkey         2         2\n\n        >>> df.rename_axis(index={\'type\': \'class\'})\n        limbs          num_legs  num_arms\n        class  name\n        mammal dog            4         0\n               cat            4         0\n               monkey         2         2\n\n        >>> df.rename_axis(columns=str.upper)\n        LIMBS          num_legs  num_arms\n        type   name\n        mammal dog            4         0\n               cat            4         0\n               monkey         2         2\n        '
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