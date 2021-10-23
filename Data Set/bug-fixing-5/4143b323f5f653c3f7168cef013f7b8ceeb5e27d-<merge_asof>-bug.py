def merge_asof(left, right, on=None, left_on=None, right_on=None, by=None, suffixes=('_x', '_y'), tolerance=None, allow_exact_matches=True):
    "Perform an asof merge. This is similar to a left-join except that we\n    match on nearest key rather than equal keys.\n\n    For each row in the left DataFrame, we select the last row in the right\n    DataFrame whose 'on' key is less than or equal to the left's key. Both\n    DataFrames must be sorted by the key.\n\n    Optionally perform group-wise merge. This searches for the nearest match\n    on the 'on' key within the same group according to 'by'.\n\n    .. versionadded:: 0.19.0\n\n    Parameters\n    ----------\n    left : DataFrame\n    right : DataFrame\n    on : label\n        Field name to join on. Must be found in both DataFrames.\n        The data MUST be ordered. Furthermore this must be a numeric column,\n        such as datetimelike, integer, or float. On or left_on/right_on\n        must be given.\n    left_on : label\n        Field name to join on in left DataFrame.\n    right_on : label\n        Field name to join on in right DataFrame.\n    by : column name\n        Group both the left and right DataFrames by the group column; perform\n        the merge operation on these pieces and recombine.\n    suffixes : 2-length sequence (tuple, list, ...)\n        Suffix to apply to overlapping column names in the left and right\n        side, respectively\n    tolerance : integer or Timedelta, optional, default None\n        select asof tolerance within this range; must be compatible\n        to the merge index.\n    allow_exact_matches : boolean, default True\n\n        - If True, allow matching the same 'on' value\n          (i.e. less-than-or-equal-to)\n        - If False, don't match the same 'on' value\n          (i.e., stricly less-than)\n\n    Returns\n    -------\n    merged : DataFrame\n\n    Examples\n    --------\n    >>> left\n        a left_val\n    0   1        a\n    1   5        b\n    2  10        c\n\n    >>> right\n       a  right_val\n    0  1          1\n    1  2          2\n    2  3          3\n    3  6          6\n    4  7          7\n\n    >>> pd.merge_asof(left, right, on='a')\n        a left_val  right_val\n    0   1        a          1\n    1   5        b          3\n    2  10        c          7\n\n    >>> pd.merge_asof(left, right, on='a', allow_exact_matches=False)\n        a left_val  right_val\n    0   1        a        NaN\n    1   5        b        3.0\n    2  10        c        7.0\n\n    For this example, we can achieve a similar result thru\n    ``pd.merge_ordered()``, though its not nearly as performant.\n\n    >>> (pd.merge_ordered(left, right, on='a')\n    ...    .ffill()\n    ...    .drop_duplicates(['left_val'])\n    ... )\n        a left_val  right_val\n    0   1        a        1.0\n    3   5        b        3.0\n    6  10        c        7.0\n\n    Here is a real-world times-series example\n\n    >>> quotes\n                         time ticker     bid     ask\n    0 2016-05-25 13:30:00.023   GOOG  720.50  720.93\n    1 2016-05-25 13:30:00.023   MSFT   51.95   51.96\n    2 2016-05-25 13:30:00.030   MSFT   51.97   51.98\n    3 2016-05-25 13:30:00.041   MSFT   51.99   52.00\n    4 2016-05-25 13:30:00.048   GOOG  720.50  720.93\n    5 2016-05-25 13:30:00.049   AAPL   97.99   98.01\n    6 2016-05-25 13:30:00.072   GOOG  720.50  720.88\n    7 2016-05-25 13:30:00.075   MSFT   52.01   52.03\n\n    >>> trades\n                         time ticker   price  quantity\n    0 2016-05-25 13:30:00.023   MSFT   51.95        75\n    1 2016-05-25 13:30:00.038   MSFT   51.95       155\n    2 2016-05-25 13:30:00.048   GOOG  720.77       100\n    3 2016-05-25 13:30:00.048   GOOG  720.92       100\n    4 2016-05-25 13:30:00.048   AAPL   98.00       100\n\n    By default we are taking the asof of the quotes\n\n    >>> pd.asof_merge(trades, quotes,\n    ...                       on='time',\n    ...                       by='ticker')\n                         time ticker   price  quantity     bid     ask\n    0 2016-05-25 13:30:00.023   MSFT   51.95        75   51.95   51.96\n    1 2016-05-25 13:30:00.038   MSFT   51.95       155   51.97   51.98\n    2 2016-05-25 13:30:00.048   GOOG  720.77       100  720.50  720.93\n    3 2016-05-25 13:30:00.048   GOOG  720.92       100  720.50  720.93\n    4 2016-05-25 13:30:00.048   AAPL   98.00       100     NaN     NaN\n\n    We only asof within 2ms betwen the quote time and the trade time\n\n    >>> pd.asof_merge(trades, quotes,\n    ...                       on='time',\n    ...                       by='ticker',\n    ...                       tolerance=pd.Timedelta('2ms'))\n                         time ticker   price  quantity     bid     ask\n    0 2016-05-25 13:30:00.023   MSFT   51.95        75   51.95   51.96\n    1 2016-05-25 13:30:00.038   MSFT   51.95       155     NaN     NaN\n    2 2016-05-25 13:30:00.048   GOOG  720.77       100  720.50  720.93\n    3 2016-05-25 13:30:00.048   GOOG  720.92       100  720.50  720.93\n    4 2016-05-25 13:30:00.048   AAPL   98.00       100     NaN     NaN\n\n    We only asof within 10ms betwen the quote time and the trade time\n    and we exclude exact matches on time. However *prior* data will\n    propogate forward\n\n    >>> pd.asof_merge(trades, quotes,\n    ...                       on='time',\n    ...                       by='ticker',\n    ...                       tolerance=pd.Timedelta('10ms'),\n    ...                       allow_exact_matches=False)\n                         time ticker   price  quantity     bid     ask\n    0 2016-05-25 13:30:00.023   MSFT   51.95        75     NaN     NaN\n    1 2016-05-25 13:30:00.038   MSFT   51.95       155   51.97   51.98\n    2 2016-05-25 13:30:00.048   GOOG  720.77       100  720.50  720.93\n    3 2016-05-25 13:30:00.048   GOOG  720.92       100  720.50  720.93\n    4 2016-05-25 13:30:00.048   AAPL   98.00       100     NaN     NaN\n\n    See also\n    --------\n    merge\n    merge_ordered\n\n    "
    op = _AsOfMerge(left, right, on=on, left_on=left_on, right_on=right_on, by=by, suffixes=suffixes, how='asof', tolerance=tolerance, allow_exact_matches=allow_exact_matches)
    return op.get_result()