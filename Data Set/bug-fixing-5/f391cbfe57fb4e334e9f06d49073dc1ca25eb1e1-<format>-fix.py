def format(self, formatter, subset=None):
    '\n        Format the text display value of cells.\n\n        .. versionadded:: 0.18.0\n\n        Parameters\n        ----------\n        formatter: str, callable, or dict\n        subset: IndexSlice\n            An argument to ``DataFrame.loc`` that restricts which elements\n            ``formatter`` is applied to.\n\n        Returns\n        -------\n        self : Styler\n\n        Notes\n        -----\n\n        ``formatter`` is either an ``a`` or a dict ``{column name: a}`` where\n        ``a`` is one of\n\n        - str: this will be wrapped in: ``a.format(x)``\n        - callable: called with the value of an individual cell\n\n        The default display value for numeric values is the "general" (``g``)\n        format with ``pd.options.display.precision`` precision.\n\n        Examples\n        --------\n\n        >>> df = pd.DataFrame(np.random.randn(4, 2), columns=[\'a\', \'b\'])\n        >>> df.style.format("{:.2%}")\n        >>> df[\'c\'] = [\'a\', \'b\', \'c\', \'d\']\n        >>> df.style.format({\'c\': str.upper})\n        '
    if (subset is None):
        row_locs = range(len(self.data))
        col_locs = range(len(self.data.columns))
    else:
        subset = _non_reducing_slice(subset)
        if (len(subset) == 1):
            subset = (subset, self.data.columns)
        sub_df = self.data.loc[subset]
        row_locs = self.data.index.get_indexer_for(sub_df.index)
        col_locs = self.data.columns.get_indexer_for(sub_df.columns)
    if isinstance(formatter, MutableMapping):
        for (col, col_formatter) in formatter.items():
            col_formatter = _maybe_wrap_formatter(col_formatter)
            col_num = self.data.columns.get_indexer_for([col])[0]
            for row_num in row_locs:
                self._display_funcs[(row_num, col_num)] = col_formatter
    else:
        locs = product(*(row_locs, col_locs))
        for (i, j) in locs:
            formatter = _maybe_wrap_formatter(formatter)
            self._display_funcs[(i, j)] = formatter
    return self