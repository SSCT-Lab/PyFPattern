

def rename_axis(self, mapper, axis=0, copy=True, inplace=False):
    '\n        Alter index and / or columns using input function or functions.\n        A scalar or list-like for ``mapper`` will alter the ``Index.name``\n        or ``MultiIndex.names`` attribute.\n        A function or dict for ``mapper`` will alter the labels.\n        Function / dict values must be unique (1-to-1). Labels not contained in\n        a dict / Series will be left as-is.\n\n        Parameters\n        ----------\n        mapper : scalar, list-like, dict-like or function, optional\n        axis : int or string, default 0\n        copy : boolean, default True\n            Also copy underlying data\n        inplace : boolean, default False\n\n        Returns\n        -------\n        renamed : type of caller\n\n        See Also\n        --------\n        pandas.NDFrame.rename\n        pandas.Index.rename\n\n        Examples\n        --------\n        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})\n        >>> df.rename_axis("foo")  # scalar, alters df.index.name\n             A  B\n        foo\n        0    1  4\n        1    2  5\n        2    3  6\n        >>> df.rename_axis(lambda x: 2 * x)  # function: alters labels\n           A  B\n        0  1  4\n        2  2  5\n        4  3  6\n        >>> df.rename_axis({"A": "ehh", "C": "see"}, axis="columns")  # mapping\n           ehh  B\n        0    1  4\n        1    2  5\n        2    3  6\n        '
    non_mapper = (is_scalar(mapper) or (is_list_like(mapper) and (not is_dict_like(mapper))))
    if non_mapper:
        return self._set_axis_name(mapper, axis=axis)
    else:
        axis = self._get_axis_name(axis)
        d = {
            'copy': copy,
            'inplace': inplace,
        }
        d[axis] = mapper
        return self.rename(**d)
