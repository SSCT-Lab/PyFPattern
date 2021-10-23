def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False):
    "\n    Convert categorical variable into dummy/indicator variables\n\n    Parameters\n    ----------\n    data : array-like, Series, or DataFrame\n    prefix : string, list of strings, or dict of strings, default None\n        String to append DataFrame column names\n        Pass a list with length equal to the number of columns\n        when calling get_dummies on a DataFrame. Alternativly, `prefix`\n        can be a dictionary mapping column names to prefixes.\n    prefix_sep : string, default '_'\n        If appending prefix, separator/delimiter to use. Or pass a\n        list or dictionary as with `prefix.`\n    dummy_na : bool, default False\n        Add a column to indicate NaNs, if False NaNs are ignored.\n    columns : list-like, default None\n        Column names in the DataFrame to be encoded.\n        If `columns` is None then all the columns with\n        `object` or `category` dtype will be converted.\n    sparse : bool, default False\n        Whether the dummy columns should be sparse or not.  Returns\n        SparseDataFrame if `data` is a Series or if all columns are included.\n        Otherwise returns a DataFrame with some SparseBlocks.\n    drop_first : bool, default False\n        Whether to get k-1 dummies out of k categorical levels by removing the\n        first level.\n\n        .. versionadded:: 0.18.0\n    Returns\n    -------\n    dummies : DataFrame or SparseDataFrame\n\n    Examples\n    --------\n    >>> import pandas as pd\n    >>> s = pd.Series(list('abca'))\n\n    >>> pd.get_dummies(s)\n       a  b  c\n    0  1  0  0\n    1  0  1  0\n    2  0  0  1\n    3  1  0  0\n\n    >>> s1 = ['a', 'b', np.nan]\n\n    >>> pd.get_dummies(s1)\n       a  b\n    0  1  0\n    1  0  1\n    2  0  0\n\n    >>> pd.get_dummies(s1, dummy_na=True)\n       a  b  NaN\n    0  1  0    0\n    1  0  1    0\n    2  0  0    1\n\n    >>> df = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],\n    ...                    'C': [1, 2, 3]})\n\n    >>> pd.get_dummies(df, prefix=['col1', 'col2'])\n       C  col1_a  col1_b  col2_a  col2_b  col2_c\n    0  1       1       0       0       1       0\n    1  2       0       1       1       0       0\n    2  3       1       0       0       0       1\n\n    >>> pd.get_dummies(pd.Series(list('abcaa')))\n       a  b  c\n    0  1  0  0\n    1  0  1  0\n    2  0  0  1\n    3  1  0  0\n    4  1  0  0\n\n    >>> pd.get_dummies(pd.Series(list('abcaa')), drop_first=True)\n       b  c\n    0  0  0\n    1  1  0\n    2  0  1\n    3  0  0\n    4  0  0\n\n    See Also\n    --------\n    Series.str.get_dummies\n    "
    from pandas.core.reshape.concat import concat
    from itertools import cycle
    if isinstance(data, DataFrame):
        if (columns is None):
            columns_to_encode = data.select_dtypes(include=['object', 'category']).columns
        else:
            columns_to_encode = columns

        def check_len(item, name):
            len_msg = "Length of '{name}' ({len_item}) did not match the length of the columns being encoded ({len_enc})."
            if is_list_like(item):
                if (not (len(item) == len(columns_to_encode))):
                    len_msg = len_msg.format(name=name, len_item=len(item), len_enc=len(columns_to_encode))
                    raise ValueError(len_msg)
        check_len(prefix, 'prefix')
        check_len(prefix_sep, 'prefix_sep')
        if isinstance(prefix, compat.string_types):
            prefix = cycle([prefix])
        if isinstance(prefix, dict):
            prefix = [prefix[col] for col in columns_to_encode]
        if (prefix is None):
            prefix = columns_to_encode
        if isinstance(prefix_sep, compat.string_types):
            prefix_sep = cycle([prefix_sep])
        elif isinstance(prefix_sep, dict):
            prefix_sep = [prefix_sep[col] for col in columns_to_encode]
        if (set(columns_to_encode) == set(data.columns)):
            with_dummies = []
        else:
            with_dummies = [data.drop(columns_to_encode, axis=1)]
        for (col, pre, sep) in zip(columns_to_encode, prefix, prefix_sep):
            dummy = _get_dummies_1d(data[col], prefix=pre, prefix_sep=sep, dummy_na=dummy_na, sparse=sparse, drop_first=drop_first)
            with_dummies.append(dummy)
        result = concat(with_dummies, axis=1)
    else:
        result = _get_dummies_1d(data, prefix, prefix_sep, dummy_na, sparse=sparse, drop_first=drop_first)
    return result