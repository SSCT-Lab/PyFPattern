def to_timedelta(arg, unit='ns', box=True, errors='raise'):
    "\n    Convert argument to timedelta\n\n    Parameters\n    ----------\n    arg : string, timedelta, list, tuple, 1-d array, or Series\n    unit : str, optional\n        Denote the unit of the input, if input is an integer. Default 'ns'.\n        Possible values:\n        {'Y', 'M', 'W', 'D', 'days', 'day', 'hours', hour', 'hr', 'h',\n        'm', 'minute', 'min', 'minutes', 'T', 'S', 'seconds', 'sec', 'second',\n        'ms', 'milliseconds', 'millisecond', 'milli', 'millis', 'L',\n        'us', 'microseconds', 'microsecond', 'micro', 'micros', 'U',\n        'ns', 'nanoseconds', 'nano', 'nanos', 'nanosecond', 'N'}\n    box : boolean, default True\n        - If True returns a Timedelta/TimedeltaIndex of the results\n        - if False returns a np.timedelta64 or ndarray of values of dtype\n          timedelta64[ns]\n    errors : {'ignore', 'raise', 'coerce'}, default 'raise'\n        - If 'raise', then invalid parsing will raise an exception\n        - If 'coerce', then invalid parsing will be set as NaT\n        - If 'ignore', then invalid parsing will return the input\n\n    Returns\n    -------\n    ret : timedelta64/arrays of timedelta64 if parsing succeeded\n\n    Examples\n    --------\n\n    Parsing a single string to a Timedelta:\n\n    >>> pd.to_timedelta('1 days 06:05:01.00003')\n    Timedelta('1 days 06:05:01.000030')\n    >>> pd.to_timedelta('15.5us')\n    Timedelta('0 days 00:00:00.000015')\n\n    Parsing a list or array of strings:\n\n    >>> pd.to_timedelta(['1 days 06:05:01.00003', '15.5us', 'nan'])\n    TimedeltaIndex(['1 days 06:05:01.000030', '0 days 00:00:00.000015', NaT],\n                   dtype='timedelta64[ns]', freq=None)\n\n    Converting numbers by specifying the `unit` keyword argument:\n\n    >>> pd.to_timedelta(np.arange(5), unit='s')\n    TimedeltaIndex(['00:00:00', '00:00:01', '00:00:02',\n                    '00:00:03', '00:00:04'],\n                   dtype='timedelta64[ns]', freq=None)\n    >>> pd.to_timedelta(np.arange(5), unit='d')\n    TimedeltaIndex(['0 days', '1 days', '2 days', '3 days', '4 days'],\n                   dtype='timedelta64[ns]', freq=None)\n\n    See Also\n    --------\n    pandas.DataFrame.astype : Cast argument to a specified dtype.\n    pandas.to_datetime : Convert argument to datetime.\n    "
    unit = parse_timedelta_unit(unit)
    if (errors not in ('ignore', 'raise', 'coerce')):
        raise ValueError("errors must be one of 'ignore', 'raise', or 'coerce'}")
    if (arg is None):
        return arg
    elif isinstance(arg, ABCSeries):
        from pandas import Series
        values = _convert_listlike(arg._values, unit=unit, box=False, errors=errors)
        return Series(values, index=arg.index, name=arg.name)
    elif isinstance(arg, ABCIndexClass):
        return _convert_listlike(arg, unit=unit, box=box, errors=errors, name=arg.name)
    elif (isinstance(arg, np.ndarray) and (arg.ndim == 0)):
        arg = arg.item()
    elif (is_list_like(arg) and (getattr(arg, 'ndim', 1) == 1)):
        return _convert_listlike(arg, unit=unit, box=box, errors=errors)
    elif (getattr(arg, 'ndim', 1) > 1):
        raise TypeError('arg must be a string, timedelta, list, tuple, 1-d array, or Series')
    return _coerce_scalar_to_timedelta_type(arg, unit=unit, box=box, errors=errors)