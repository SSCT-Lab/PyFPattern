def _set_axis_name(self, name, axis=0, inplace=False):
    '\n        Alter the name or names of the axis.\n\n        Parameters\n        ----------\n        name : str or list of str\n            Name for the Index, or list of names for the MultiIndex\n        axis : int or str\n           0 or \'index\' for the index; 1 or \'columns\' for the columns\n        inplace : bool\n            whether to modify `self` directly or return a copy\n\n            .. versionadded:: 0.21.0\n\n        Returns\n        -------\n        renamed : same type as caller or None if inplace=True\n\n        See Also\n        --------\n        pandas.DataFrame.rename\n        pandas.Series.rename\n        pandas.Index.rename\n\n        Examples\n        --------\n        >>> df._set_axis_name("foo")\n             A\n        foo\n        0    1\n        1    2\n        2    3\n        >>> df.index = pd.MultiIndex.from_product([[\'A\'], [\'a\', \'b\', \'c\']])\n        >>> df._set_axis_name(["bar", "baz"])\n                 A\n        bar baz\n        A   a    1\n            b    2\n            c    3\n        '
    axis = self._get_axis_number(axis)
    idx = self._get_axis(axis).set_names(name)
    inplace = validate_bool_kwarg(inplace, 'inplace')
    renamed = (self if inplace else self.copy())
    renamed.set_axis(idx, axis=axis, inplace=True)
    if (not inplace):
        return renamed