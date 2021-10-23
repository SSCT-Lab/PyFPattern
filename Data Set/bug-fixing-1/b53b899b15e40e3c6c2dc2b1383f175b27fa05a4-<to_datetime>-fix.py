

@deprecate_kwarg(old_arg_name='box', new_arg_name=None)
def to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, utc=None, box=True, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True):
    '\n    Convert argument to datetime.\n\n    Parameters\n    ----------\n    arg : int, float, str, datetime, list, tuple, 1-d array, Series\n           or DataFrame/dict-like\n\n    errors : {\'ignore\', \'raise\', \'coerce\'}, default \'raise\'\n\n        - If \'raise\', then invalid parsing will raise an exception\n        - If \'coerce\', then invalid parsing will be set as NaT\n        - If \'ignore\', then invalid parsing will return the input\n    dayfirst : bool, default False\n        Specify a date parse order if `arg` is str or its list-likes.\n        If True, parses dates with the day first, eg 10/11/12 is parsed as\n        2012-11-10.\n        Warning: dayfirst=True is not strict, but will prefer to parse\n        with day first (this is a known bug, based on dateutil behavior).\n    yearfirst : bool, default False\n        Specify a date parse order if `arg` is str or its list-likes.\n\n        - If True parses dates with the year first, eg 10/11/12 is parsed as\n          2010-11-12.\n        - If both dayfirst and yearfirst are True, yearfirst is preceded (same\n          as dateutil).\n\n        Warning: yearfirst=True is not strict, but will prefer to parse\n        with year first (this is a known bug, based on dateutil behavior).\n\n        .. versionadded:: 0.16.1\n\n    utc : bool, default None\n        Return UTC DatetimeIndex if True (converting any tz-aware\n        datetime.datetime objects as well).\n    box : bool, default True\n\n        - If True returns a DatetimeIndex or Index-like object\n        - If False returns ndarray of values.\n\n        .. deprecated:: 0.25.0\n            Use :meth:`Series.to_numpy` or :meth:`Timestamp.to_datetime64`\n            instead to get an ndarray of values or numpy.datetime64,\n            respectively.\n\n    format : str, default None\n        strftime to parse time, eg "%d/%m/%Y", note that "%f" will parse\n        all the way up to nanoseconds.\n        See strftime documentation for more information on choices:\n        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior\n    exact : bool, True by default\n\n        - If True, require an exact format match.\n        - If False, allow the format to match anywhere in the target string.\n\n    unit : str, default \'ns\'\n        unit of the arg (D,s,ms,us,ns) denote the unit, which is an\n        integer or float number. This will be based off the origin.\n        Example, with unit=\'ms\' and origin=\'unix\' (the default), this\n        would calculate the number of milliseconds to the unix epoch start.\n    infer_datetime_format : bool, default False\n        If True and no `format` is given, attempt to infer the format of the\n        datetime strings, and if it can be inferred, switch to a faster\n        method of parsing them. In some cases this can increase the parsing\n        speed by ~5-10x.\n    origin : scalar, default \'unix\'\n        Define the reference date. The numeric values would be parsed as number\n        of units (defined by `unit`) since this reference date.\n\n        - If \'unix\' (or POSIX) time; origin is set to 1970-01-01.\n        - If \'julian\', unit must be \'D\', and origin is set to beginning of\n          Julian Calendar. Julian day number 0 is assigned to the day starting\n          at noon on January 1, 4713 BC.\n        - If Timestamp convertible, origin is set to Timestamp identified by\n          origin.\n\n        .. versionadded:: 0.20.0\n    cache : bool, default True\n        If True, use a cache of unique, converted dates to apply the datetime\n        conversion. May produce significant speed-up when parsing duplicate\n        date strings, especially ones with timezone offsets.\n\n        .. versionadded:: 0.23.0\n\n        .. versionchanged:: 0.25.0\n            - changed default value from False to True\n\n    Returns\n    -------\n    ret : datetime if parsing succeeded.\n        Return type depends on input:\n\n        - list-like: DatetimeIndex\n        - Series: Series of datetime64 dtype\n        - scalar: Timestamp\n\n        In case when it is not possible to return designated types (e.g. when\n        any element of input is before Timestamp.min or after Timestamp.max)\n        return will have datetime.datetime type (or corresponding\n        array/Series).\n\n    See Also\n    --------\n    DataFrame.astype : Cast argument to a specified dtype.\n    to_timedelta : Convert argument to timedelta.\n\n    Examples\n    --------\n    Assembling a datetime from multiple columns of a DataFrame. The keys can be\n    common abbreviations like [\'year\', \'month\', \'day\', \'minute\', \'second\',\n    \'ms\', \'us\', \'ns\']) or plurals of the same\n\n    >>> df = pd.DataFrame({\'year\': [2015, 2016],\n    ...                    \'month\': [2, 3],\n    ...                    \'day\': [4, 5]})\n    >>> pd.to_datetime(df)\n    0   2015-02-04\n    1   2016-03-05\n    dtype: datetime64[ns]\n\n    If a date does not meet the `timestamp limitations\n    <http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html\n    #timeseries-timestamp-limits>`_, passing errors=\'ignore\'\n    will return the original input instead of raising any exception.\n\n    Passing errors=\'coerce\' will force an out-of-bounds date to NaT,\n    in addition to forcing non-dates (or non-parseable dates) to NaT.\n\n    >>> pd.to_datetime(\'13000101\', format=\'%Y%m%d\', errors=\'ignore\')\n    datetime.datetime(1300, 1, 1, 0, 0)\n    >>> pd.to_datetime(\'13000101\', format=\'%Y%m%d\', errors=\'coerce\')\n    NaT\n\n    Passing infer_datetime_format=True can often-times speedup a parsing\n    if its not an ISO8601 format exactly, but in a regular format.\n\n    >>> s = pd.Series([\'3/11/2000\', \'3/12/2000\', \'3/13/2000\'] * 1000)\n    >>> s.head()\n    0    3/11/2000\n    1    3/12/2000\n    2    3/13/2000\n    3    3/11/2000\n    4    3/12/2000\n    dtype: object\n\n    >>> %timeit pd.to_datetime(s,infer_datetime_format=True)  # doctest: +SKIP\n    100 loops, best of 3: 10.4 ms per loop\n\n    >>> %timeit pd.to_datetime(s,infer_datetime_format=False)  # doctest: +SKIP\n    1 loop, best of 3: 471 ms per loop\n\n    Using a unix epoch time\n\n    >>> pd.to_datetime(1490195805, unit=\'s\')\n    Timestamp(\'2017-03-22 15:16:45\')\n    >>> pd.to_datetime(1490195805433502912, unit=\'ns\')\n    Timestamp(\'2017-03-22 15:16:45.433502912\')\n\n    .. warning:: For float arg, precision rounding might happen. To prevent\n        unexpected behavior use a fixed-width exact type.\n\n    Using a non-unix epoch origin\n\n    >>> pd.to_datetime([1, 2, 3], unit=\'D\',\n    ...                origin=pd.Timestamp(\'1960-01-01\'))\n    DatetimeIndex([\'1960-01-02\', \'1960-01-03\', \'1960-01-04\'], dtype=\'datetime64[ns]\', freq=None)\n    '
    if (arg is None):
        return None
    if (origin != 'unix'):
        arg = _adjust_to_origin(arg, origin, unit)
    tz = ('utc' if utc else None)
    convert_listlike = partial(_convert_listlike_datetimes, tz=tz, unit=unit, dayfirst=dayfirst, yearfirst=yearfirst, errors=errors, exact=exact, infer_datetime_format=infer_datetime_format)
    if isinstance(arg, Timestamp):
        result = arg
        if (tz is not None):
            if (arg.tz is not None):
                result = result.tz_convert(tz)
            else:
                result = result.tz_localize(tz)
    elif isinstance(arg, ABCSeries):
        cache_array = _maybe_cache(arg, format, cache, convert_listlike)
        if (not cache_array.empty):
            result = arg.map(cache_array)
        else:
            values = convert_listlike(arg._values, True, format)
            result = arg._constructor(values, index=arg.index, name=arg.name)
    elif isinstance(arg, (ABCDataFrame, abc.MutableMapping)):
        result = _assemble_from_unit_mappings(arg, errors, box, tz)
    elif isinstance(arg, ABCIndexClass):
        cache_array = _maybe_cache(arg, format, cache, convert_listlike)
        if (not cache_array.empty):
            result = _convert_and_box_cache(arg, cache_array, box, name=arg.name)
        else:
            convert_listlike = partial(convert_listlike, name=arg.name)
            result = convert_listlike(arg, box, format)
    elif is_list_like(arg):
        cache_array = _maybe_cache(arg, format, cache, convert_listlike)
        if (not cache_array.empty):
            result = _convert_and_box_cache(arg, cache_array, box)
        else:
            result = convert_listlike(arg, box, format)
    else:
        result = convert_listlike(np.array([arg]), box, format)[0]
    return result
