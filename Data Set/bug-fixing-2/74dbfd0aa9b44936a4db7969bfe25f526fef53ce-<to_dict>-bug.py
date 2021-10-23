

def to_dict(self, orient='dict', into=dict):
    "Convert DataFrame to dictionary.\n\n        Parameters\n        ----------\n        orient : str {'dict', 'list', 'series', 'split', 'records', 'index'}\n            Determines the type of the values of the dictionary.\n\n            - dict (default) : dict like {column -> {index -> value}}\n            - list : dict like {column -> [values]}\n            - series : dict like {column -> Series(values)}\n            - split : dict like\n              {index -> [index], columns -> [columns], data -> [values]}\n            - records : list like\n              [{column -> value}, ... , {column -> value}]\n            - index : dict like {index -> {column -> value}}\n\n            Abbreviations are allowed. `s` indicates `series` and `sp`\n            indicates `split`.\n\n        into : class, default dict\n            The collections.Mapping subclass used for all Mappings\n            in the return value.  Can be the actual class or an empty\n            instance of the mapping type you want.  If you want a\n            collections.defaultdict, you must pass it initialized.\n\n            .. versionadded:: 0.21.0\n\n        Returns\n        -------\n        result : collections.Mapping like {column -> {index -> value}}\n\n        Examples\n        --------\n        >>> df = pd.DataFrame(\n                {'col1': [1, 2], 'col2': [0.5, 0.75]}, index=['a', 'b'])\n        >>> df\n           col1  col2\n        a     1   0.1\n        b     2   0.2\n        >>> df.to_dict()\n        {'col1': {'a': 1, 'b': 2}, 'col2': {'a': 0.5, 'b': 0.75}}\n\n        You can specify the return orientation.\n\n        >>> df.to_dict('series')\n        {'col1': a    1\n        b    2\n        Name: col1, dtype: int64, 'col2': a    0.50\n        b    0.75\n        Name: col2, dtype: float64}\n        >>> df.to_dict('split')\n        {'columns': ['col1', 'col2'],\n        'data': [[1.0, 0.5], [2.0, 0.75]],\n        'index': ['a', 'b']}\n        >>> df.to_dict('records')\n        [{'col1': 1.0, 'col2': 0.5}, {'col1': 2.0, 'col2': 0.75}]\n        >>> df.to_dict('index')\n        {'a': {'col1': 1.0, 'col2': 0.5}, 'b': {'col1': 2.0, 'col2': 0.75}}\n\n        You can also specify the mapping type.\n\n        >>> from collections import OrderedDict, defaultdict\n        >>> df.to_dict(into=OrderedDict)\n        OrderedDict([('col1', OrderedDict([('a', 1), ('b', 2)])),\n                   ('col2', OrderedDict([('a', 0.5), ('b', 0.75)]))])\n\n        If you want a `defaultdict`, you need to initialize it:\n\n        >>> dd = defaultdict(list)\n        >>> df.to_dict('records', into=dd)\n        [defaultdict(<type 'list'>, {'col2': 0.5, 'col1': 1.0}),\n        defaultdict(<type 'list'>, {'col2': 0.75, 'col1': 2.0})]\n        "
    if (not self.columns.is_unique):
        warnings.warn('DataFrame columns are not unique, some columns will be omitted.', UserWarning, stacklevel=2)
    into_c = com.standardize_mapping(into)
    if orient.lower().startswith('d'):
        return into_c(((k, v.to_dict(into)) for (k, v) in compat.iteritems(self)))
    elif orient.lower().startswith('l'):
        return into_c(((k, v.tolist()) for (k, v) in compat.iteritems(self)))
    elif orient.lower().startswith('sp'):
        return into_c((('index', self.index.tolist()), ('columns', self.columns.tolist()), ('data', lib.map_infer(self.values.ravel(), com._maybe_box_datetimelike).reshape(self.values.shape).tolist())))
    elif orient.lower().startswith('s'):
        return into_c(((k, com._maybe_box_datetimelike(v)) for (k, v) in compat.iteritems(self)))
    elif orient.lower().startswith('r'):
        return [into_c(((k, com._maybe_box_datetimelike(v)) for (k, v) in zip(self.columns, np.atleast_1d(row)))) for row in self.values]
    elif orient.lower().startswith('i'):
        return into_c(((k, v.to_dict(into)) for (k, v) in self.iterrows()))
    else:
        raise ValueError(("orient '%s' not understood" % orient))
