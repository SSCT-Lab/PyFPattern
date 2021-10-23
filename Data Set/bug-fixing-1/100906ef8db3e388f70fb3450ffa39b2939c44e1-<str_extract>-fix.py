

def str_extract(arr, pat, flags=0, expand=True):
    "\n    Extract capture groups in the regex `pat` as columns in a DataFrame.\n\n    For each subject string in the Series, extract groups from the\n    first match of regular expression `pat`.\n\n    Parameters\n    ----------\n    pat : string\n        Regular expression pattern with capturing groups.\n    flags : int, default 0 (no flags)\n        Flags from the ``re`` module, e.g. ``re.IGNORECASE``, that\n        modify regular expression matching for things like case,\n        spaces, etc. For more details, see :mod:`re`.\n    expand : bool, default True\n        If True, return DataFrame with one column per capture group.\n        If False, return a Series/Index if there is one capture group\n        or DataFrame if there are multiple capture groups.\n\n        .. versionadded:: 0.18.0\n\n    Returns\n    -------\n    DataFrame or Series or Index\n        A DataFrame with one row for each subject string, and one\n        column for each group. Any capture group names in regular\n        expression pat will be used for column names; otherwise\n        capture group numbers will be used. The dtype of each result\n        column is always object, even when no match is found. If\n        ``expand=False`` and pat has only one capture group, then\n        return a Series (if subject is a Series) or Index (if subject\n        is an Index).\n\n    See Also\n    --------\n    extractall : returns all matches (not just the first match)\n\n    Examples\n    --------\n    A pattern with two groups will return a DataFrame with two columns.\n    Non-matches will be NaN.\n\n    >>> s = pd.Series(['a1', 'b2', 'c3'])\n    >>> s.str.extract(r'([ab])(\\d)')\n         0    1\n    0    a    1\n    1    b    2\n    2  NaN  NaN\n\n    A pattern may contain optional groups.\n\n    >>> s.str.extract(r'([ab])?(\\d)')\n         0  1\n    0    a  1\n    1    b  2\n    2  NaN  3\n\n    Named groups will become column names in the result.\n\n    >>> s.str.extract(r'(?P<letter>[ab])(?P<digit>\\d)')\n      letter digit\n    0      a     1\n    1      b     2\n    2    NaN   NaN\n\n    A pattern with one group will return a DataFrame with one column\n    if expand=True.\n\n    >>> s.str.extract(r'[ab](\\d)', expand=True)\n         0\n    0    1\n    1    2\n    2  NaN\n\n    A pattern with one group will return a Series if expand=False.\n\n    >>> s.str.extract(r'[ab](\\d)', expand=False)\n    0      1\n    1      2\n    2    NaN\n    dtype: object\n    "
    if (not isinstance(expand, bool)):
        raise ValueError('expand must be True or False')
    if expand:
        return _str_extract_frame(arr._orig, pat, flags=flags)
    else:
        (result, name) = _str_extract_noexpand(arr._parent, pat, flags=flags)
        return arr._wrap_result(result, name=name, expand=expand)
