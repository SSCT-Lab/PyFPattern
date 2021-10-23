

def concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
    '\n    Concatenate pandas objects along a particular axis with optional set logic\n    along the other axes.\n\n    Can also add a layer of hierarchical indexing on the concatenation axis,\n    which may be useful if the labels are the same (or overlapping) on\n    the passed axis number.\n\n    Parameters\n    ----------\n    objs : a sequence or mapping of Series, DataFrame, or Panel objects\n        If a dict is passed, the sorted keys will be used as the `keys`\n        argument, unless it is passed, in which case the values will be\n        selected (see below). Any None objects will be dropped silently unless\n        they are all None in which case a ValueError will be raised\n    axis : {0/\'index\', 1/\'columns\'}, default 0\n        The axis to concatenate along\n    join : {\'inner\', \'outer\'}, default \'outer\'\n        How to handle indexes on other axis(es)\n    join_axes : list of Index objects\n        Specific indexes to use for the other n - 1 axes instead of performing\n        inner/outer set logic\n    ignore_index : boolean, default False\n        If True, do not use the index values along the concatenation axis. The\n        resulting axis will be labeled 0, ..., n - 1. This is useful if you are\n        concatenating objects where the concatenation axis does not have\n        meaningful indexing information. Note the index values on the other\n        axes are still respected in the join.\n    keys : sequence, default None\n        If multiple levels passed, should contain tuples. Construct\n        hierarchical index using the passed keys as the outermost level\n    levels : list of sequences, default None\n        Specific levels (unique values) to use for constructing a\n        MultiIndex. Otherwise they will be inferred from the keys\n    names : list, default None\n        Names for the levels in the resulting hierarchical index\n    verify_integrity : boolean, default False\n        Check whether the new concatenated axis contains duplicates. This can\n        be very expensive relative to the actual data concatenation\n    sort : boolean, default None\n        Sort non-concatenation axis if it is not already aligned when `join`\n        is \'outer\'. The current default of sorting is deprecated and will\n        change to not-sorting in a future version of pandas.\n\n        Explicitly pass ``sort=True`` to silence the warning and sort.\n        Explicitly pass ``sort=False`` to silence the warning and not sort.\n\n        This has no effect when ``join=\'inner\'``, which already preserves\n        the order of the non-concatenation axis.\n\n        .. versionadded:: 0.23.0\n\n    copy : boolean, default True\n        If False, do not copy data unnecessarily\n\n    Returns\n    -------\n    concatenated : object, type of objs\n        When concatenating all ``Series`` along the index (axis=0), a\n        ``Series`` is returned. When ``objs`` contains at least one\n        ``DataFrame``, a ``DataFrame`` is returned. When concatenating along\n        the columns (axis=1), a ``DataFrame`` is returned.\n\n    Notes\n    -----\n    The keys, levels, and names arguments are all optional.\n\n    A walkthrough of how this method fits in with other tools for combining\n    pandas objects can be found `here\n    <http://pandas.pydata.org/pandas-docs/stable/merging.html>`__.\n\n    See Also\n    --------\n    Series.append\n    DataFrame.append\n    DataFrame.join\n    DataFrame.merge\n\n    Examples\n    --------\n    Combine two ``Series``.\n\n    >>> s1 = pd.Series([\'a\', \'b\'])\n    >>> s2 = pd.Series([\'c\', \'d\'])\n    >>> pd.concat([s1, s2])\n    0    a\n    1    b\n    0    c\n    1    d\n    dtype: object\n\n    Clear the existing index and reset it in the result\n    by setting the ``ignore_index`` option to ``True``.\n\n    >>> pd.concat([s1, s2], ignore_index=True)\n    0    a\n    1    b\n    2    c\n    3    d\n    dtype: object\n\n    Add a hierarchical index at the outermost level of\n    the data with the ``keys`` option.\n\n    >>> pd.concat([s1, s2], keys=[\'s1\', \'s2\',])\n    s1  0    a\n        1    b\n    s2  0    c\n        1    d\n    dtype: object\n\n    Label the index keys you create with the ``names`` option.\n\n    >>> pd.concat([s1, s2], keys=[\'s1\', \'s2\'],\n    ...           names=[\'Series name\', \'Row ID\'])\n    Series name  Row ID\n    s1           0         a\n                 1         b\n    s2           0         c\n                 1         d\n    dtype: object\n\n    Combine two ``DataFrame`` objects with identical columns.\n\n    >>> df1 = pd.DataFrame([[\'a\', 1], [\'b\', 2]],\n    ...                    columns=[\'letter\', \'number\'])\n    >>> df1\n      letter  number\n    0      a       1\n    1      b       2\n    >>> df2 = pd.DataFrame([[\'c\', 3], [\'d\', 4]],\n    ...                    columns=[\'letter\', \'number\'])\n    >>> df2\n      letter  number\n    0      c       3\n    1      d       4\n    >>> pd.concat([df1, df2])\n      letter  number\n    0      a       1\n    1      b       2\n    0      c       3\n    1      d       4\n\n    Combine ``DataFrame`` objects with overlapping columns\n    and return everything. Columns outside the intersection will\n    be filled with ``NaN`` values.\n\n    >>> df3 = pd.DataFrame([[\'c\', 3, \'cat\'], [\'d\', 4, \'dog\']],\n    ...                    columns=[\'letter\', \'number\', \'animal\'])\n    >>> df3\n      letter  number animal\n    0      c       3    cat\n    1      d       4    dog\n    >>> pd.concat([df1, df3])\n      animal letter  number\n    0    NaN      a       1\n    1    NaN      b       2\n    0    cat      c       3\n    1    dog      d       4\n\n    Combine ``DataFrame`` objects with overlapping columns\n    and return only those that are shared by passing ``inner`` to\n    the ``join`` keyword argument.\n\n    >>> pd.concat([df1, df3], join="inner")\n      letter  number\n    0      a       1\n    1      b       2\n    0      c       3\n    1      d       4\n\n    Combine ``DataFrame`` objects horizontally along the x axis by\n    passing in ``axis=1``.\n\n    >>> df4 = pd.DataFrame([[\'bird\', \'polly\'], [\'monkey\', \'george\']],\n    ...                    columns=[\'animal\', \'name\'])\n    >>> pd.concat([df1, df4], axis=1)\n      letter  number  animal    name\n    0      a       1    bird   polly\n    1      b       2  monkey  george\n\n    Prevent the result from including duplicate index values with the\n    ``verify_integrity`` option.\n\n    >>> df5 = pd.DataFrame([1], index=[\'a\'])\n    >>> df5\n       0\n    a  1\n    >>> df6 = pd.DataFrame([2], index=[\'a\'])\n    >>> df6\n       0\n    a  2\n    >>> pd.concat([df5, df6], verify_integrity=True)\n    Traceback (most recent call last):\n        ...\n    ValueError: Indexes have overlapping values: [\'a\']\n    '
    op = _Concatenator(objs, axis=axis, join_axes=join_axes, ignore_index=ignore_index, join=join, keys=keys, levels=levels, names=names, verify_integrity=verify_integrity, copy=copy, sort=sort)
    return op.get_result()
