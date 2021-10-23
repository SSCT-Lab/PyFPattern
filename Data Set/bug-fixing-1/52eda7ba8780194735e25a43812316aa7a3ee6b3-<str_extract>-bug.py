

def str_extract(arr, pat, flags=0, expand=None):
    "\n    For each subject string in the Series, extract groups from the\n    first match of regular expression pat.\n\n    .. versionadded:: 0.13.0\n\n    Parameters\n    ----------\n    pat : string\n        Regular expression pattern with capturing groups\n    flags : int, default 0 (no flags)\n        re module flags, e.g. re.IGNORECASE\n\n    .. versionadded:: 0.18.0\n    expand : bool, default False\n        * If True, return DataFrame.\n        * If False, return Series/Index/DataFrame.\n\n    Returns\n    -------\n    DataFrame with one row for each subject string, and one column for\n    each group. Any capture group names in regular expression pat will\n    be used for column names; otherwise capture group numbers will be\n    used. The dtype of each result column is always object, even when\n    no match is found. If expand=False and pat has only one capture group,\n    then return a Series (if subject is a Series) or Index (if subject\n    is an Index).\n\n    See Also\n    --------\n    extractall : returns all matches (not just the first match)\n\n    Examples\n    --------\n    A pattern with two groups will return a DataFrame with two columns.\n    Non-matches will be NaN.\n\n    >>> s = Series(['a1', 'b2', 'c3'])\n    >>> s.str.extract('([ab])(\\d)')\n         0    1\n    0    a    1\n    1    b    2\n    2  NaN  NaN\n\n    A pattern may contain optional groups.\n\n    >>> s.str.extract('([ab])?(\\d)')\n         0  1\n    0    a  1\n    1    b  2\n    2  NaN  3\n\n    Named groups will become column names in the result.\n\n    >>> s.str.extract('(?P<letter>[ab])(?P<digit>\\d)')\n      letter digit\n    0      a     1\n    1      b     2\n    2    NaN   NaN\n\n    A pattern with one group will return a DataFrame with one column\n    if expand=True.\n\n    >>> s.str.extract('[ab](\\d)', expand=True)\n         0\n    0    1\n    1    2\n    2  NaN\n\n    A pattern with one group will return a Series if expand=False.\n\n    >>> s.str.extract('[ab](\\d)', expand=False)\n    0      1\n    1      2\n    2    NaN\n    dtype: object\n\n    "
    if (expand is None):
        warnings.warn(((('currently extract(expand=None) ' + 'means expand=False (return Index/Series/DataFrame) ') + 'but in a future version of pandas this will be changed ') + 'to expand=True (return DataFrame)'), FutureWarning, stacklevel=3)
        expand = False
    if (not isinstance(expand, bool)):
        raise ValueError('expand must be True or False')
    if expand:
        return _str_extract_frame(arr._orig, pat, flags=flags)
    else:
        (result, name) = _str_extract_noexpand(arr._data, pat, flags=flags)
        return arr._wrap_result(result, name=name, expand=expand)
