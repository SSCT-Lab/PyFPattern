

def period_range(start=None, end=None, periods=None, freq=None, name=None):
    '\n    Return a fixed frequency PeriodIndex, with day (calendar) as the default\n    frequency.\n\n    Parameters\n    ----------\n    start : string or period-like, default None\n        Left bound for generating periods\n    end : string or period-like, default None\n        Right bound for generating periods\n    periods : integer, default None\n        Number of periods to generate\n    freq : string or DateOffset, optional\n        Frequency alias. By default the freq is taken from `start` or `end`\n        if those are Period objects. Otherwise, the default is ``"D"`` for\n        daily frequency.\n\n    name : string, default None\n        Name of the resulting PeriodIndex\n\n    Returns\n    -------\n    prng : PeriodIndex\n\n    Notes\n    -----\n    Of the three parameters: ``start``, ``end``, and ``periods``, exactly two\n    must be specified.\n\n    To learn more about the frequency strings, please see `this link\n    <http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`__.\n\n    Examples\n    --------\n\n    >>> pd.period_range(start=\'2017-01-01\', end=\'2018-01-01\', freq=\'M\')\n    PeriodIndex([\'2017-01\', \'2017-02\', \'2017-03\', \'2017-04\', \'2017-05\',\n                 \'2017-06\', \'2017-06\', \'2017-07\', \'2017-08\', \'2017-09\',\n                 \'2017-10\', \'2017-11\', \'2017-12\', \'2018-01\'],\n                dtype=\'period[M]\', freq=\'M\')\n\n    If ``start`` or ``end`` are ``Period`` objects, they will be used as anchor\n    endpoints for a ``PeriodIndex`` with frequency matching that of the\n    ``period_range`` constructor.\n\n    >>> pd.period_range(start=pd.Period(\'2017Q1\', freq=\'Q\'),\n    ...                 end=pd.Period(\'2017Q2\', freq=\'Q\'), freq=\'M\')\n    PeriodIndex([\'2017-03\', \'2017-04\', \'2017-05\', \'2017-06\'],\n                dtype=\'period[M]\', freq=\'M\')\n    '
    if (com.count_not_none(start, end, periods) != 2):
        raise ValueError('Of the three parameters: start, end, and periods, exactly two must be specified')
    if ((freq is None) and ((not isinstance(start, Period)) and (not isinstance(end, Period)))):
        freq = 'D'
    (data, freq) = PeriodArray._generate_range(start, end, periods, freq, fields={
        
    })
    data = PeriodArray(data, freq=freq)
    return PeriodIndex(data, name=name)
