def to_timedelta(arg, unit='ns', box=True, errors='raise'):
    "\n    Convert argument to timedelta.\n\n    Timedeltas are absolute differences in times, expressed in difference\n    units (e.g. days, hours, minutes, seconds). This method converts\n    an argument from a recognized timedelta format / value into\n    a Timedelta type.\n\n    Parameters\n    ----------\n    arg : str, timedelta, list-like or Series\n        The data to be converted to timedelta.\n    unit : str, default 'ns'\n        Denotes the unit of the arg. Possible values:\n        ('Y', 'M', 'W', 'D', 'days', 'day', 'hours', hour', 'hr',\n        'h', 'm', 'minute', 'min', 'minutes', 'T', 'S', 'seconds',\n        'sec', 'second', 'ms', 'milliseconds', 'millisecond',\n        'milli', 'millis', 'L', 'us', 'microseconds', 'microsecond',\n        'micro', 'micros', 'U', 'ns', 'nanoseconds', 'nano', 'nanos',\n        'nanosecond', 'N').\n    box : bool, default True\n        - If True returns a Timedelta/TimedeltaIndex of the results.\n        - If False returns a numpy.timedelta64 or numpy.darray of\n          values of dtype timedelta64[ns].\n    errors : {'ignore', 'raise', 'coerce'}, default 'raise'\n        - If 'raise', then invalid parsing will raise an exception.\n        - If 'coerce', then invalid parsing will be set as NaT.\n        - If 'ignore', then invalid parsing will return the input.\n\n    Returns\n    -------\n    timedelta64 or numpy.array of timedelta64\n        Output type returned if parsing succeeded.\n\n    See also\n    --------\n    DataFrame.astype : Cast argument to a specified dtype.\n    to_datetime : Convert argument to datetime.\n\n    Examples\n    --------\n\n    Parsing a single string to a Timedelta:\n\n    >>> pd.to_timedelta('1 days 06:05:01.00003')\n    Timedelta('1 days 06:05:01.000030')\n    >>> pd.to_timedelta('15.5us')\n    Timedelta('0 days 00:00:00.000015')\n\n    Parsing a list or array of strings:\n\n    >>> pd.to_timedelta(['1 days 06:05:01.00003', '15.5us', 'nan'])\n    TimedeltaIndex(['1 days 06:05:01.000030', '0 days 00:00:00.000015', NaT],\n                   dtype='timedelta64[ns]', freq=None)\n\n    Converting numbers by specifying the `unit` keyword argument:\n\n    >>> pd.to_timedelta(np.arange(5), unit='s')\n    TimedeltaIndex(['00:00:00', '00:00:01', '00:00:02',\n                    '00:00:03', '00:00:04'],\n                   dtype='timedelta64[ns]', freq=None)\n    >>> pd.to_timedelta(np.arange(5), unit='d')\n    TimedeltaIndex(['0 days', '1 days', '2 days', '3 days', '4 days'],\n                   dtype='timedelta64[ns]', freq=None)\n\n    Returning an ndarray by using the 'box' keyword argument:\n\n    >>> pd.to_timedelta(np.arange(5), box=False)\n    array([0, 1, 2, 3, 4], dtype='timedelta64[ns]')\n    "
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