

def tz_localize(self, tz, axis=0, level=None, copy=True, ambiguous='raise', nonexistent='raise'):
    "\n        Localize tz-naive index of a Series or DataFrame to target time zone.\n\n        This operation localizes the Index. To localize the values in a\n        timezone-naive Series, use :meth:`Series.dt.tz_localize`.\n\n        Parameters\n        ----------\n        tz : string or pytz.timezone object\n        axis : the axis to localize\n        level : int, str, default None\n            If axis ia a MultiIndex, localize a specific level. Otherwise\n            must be None\n        copy : boolean, default True\n            Also make a copy of the underlying data\n        ambiguous : 'infer', bool-ndarray, 'NaT', default 'raise'\n            When clocks moved backward due to DST, ambiguous times may arise.\n            For example in Central European Time (UTC+01), when going from\n            03:00 DST to 02:00 non-DST, 02:30:00 local time occurs both at\n            00:30:00 UTC and at 01:30:00 UTC. In such a situation, the\n            `ambiguous` parameter dictates how ambiguous times should be\n            handled.\n\n            - 'infer' will attempt to infer fall dst-transition hours based on\n              order\n            - bool-ndarray where True signifies a DST time, False designates\n              a non-DST time (note that this flag is only applicable for\n              ambiguous times)\n            - 'NaT' will return NaT where there are ambiguous times\n            - 'raise' will raise an AmbiguousTimeError if there are ambiguous\n              times\n        nonexistent : str, default 'raise'\n            A nonexistent time does not exist in a particular timezone\n            where clocks moved forward due to DST. Valid valuse are:\n\n            - 'shift_forward' will shift the nonexistent time forward to the\n              closest existing time\n            - 'shift_backward' will shift the nonexistent time backward to the\n              closest existing time\n            - 'NaT' will return NaT where there are nonexistent times\n            - timedelta objects will shift nonexistent times by the timedelta\n            - 'raise' will raise an NonExistentTimeError if there are\n              nonexistent times\n\n            .. versionadded:: 0.24.0\n\n        Returns\n        -------\n        Series or DataFrame\n            Same type as the input.\n\n        Raises\n        ------\n        TypeError\n            If the TimeSeries is tz-aware and tz is not None.\n\n        Examples\n        --------\n\n        Localize local times:\n\n        >>> s = pd.Series([1],\n        ... index=pd.DatetimeIndex(['2018-09-15 01:30:00']))\n        >>> s.tz_localize('CET')\n        2018-09-15 01:30:00+02:00    1\n        dtype: int64\n\n        Be careful with DST changes. When there is sequential data, pandas\n        can infer the DST time:\n\n        >>> s = pd.Series(range(7), index=pd.DatetimeIndex([\n        ... '2018-10-28 01:30:00',\n        ... '2018-10-28 02:00:00',\n        ... '2018-10-28 02:30:00',\n        ... '2018-10-28 02:00:00',\n        ... '2018-10-28 02:30:00',\n        ... '2018-10-28 03:00:00',\n        ... '2018-10-28 03:30:00']))\n        >>> s.tz_localize('CET', ambiguous='infer')\n        2018-10-28 01:30:00+02:00    0\n        2018-10-28 02:00:00+02:00    1\n        2018-10-28 02:30:00+02:00    2\n        2018-10-28 02:00:00+01:00    3\n        2018-10-28 02:30:00+01:00    4\n        2018-10-28 03:00:00+01:00    5\n        2018-10-28 03:30:00+01:00    6\n        dtype: int64\n\n        In some cases, inferring the DST is impossible. In such cases, you can\n        pass an ndarray to the ambiguous parameter to set the DST explicitly\n\n        >>> s = pd.Series(range(3), index=pd.DatetimeIndex([\n        ... '2018-10-28 01:20:00',\n        ... '2018-10-28 02:36:00',\n        ... '2018-10-28 03:46:00']))\n        >>> s.tz_localize('CET', ambiguous=np.array([True, True, False]))\n        2018-10-28 01:20:00+02:00    0\n        2018-10-28 02:36:00+02:00    1\n        2018-10-28 03:46:00+01:00    2\n        dtype: int64\n\n        If the DST transition causes nonexistent times, you can shift these\n        dates forward or backwards with a timedelta object or `'shift_forward'`\n        or `'shift_backwards'`.\n        >>> s = pd.Series(range(2), index=pd.DatetimeIndex([\n        ... '2015-03-29 02:30:00',\n        ... '2015-03-29 03:30:00']))\n        >>> s.tz_localize('Europe/Warsaw', nonexistent='shift_forward')\n        2015-03-29 03:00:00+02:00    0\n        2015-03-29 03:30:00+02:00    1\n        dtype: int64\n        >>> s.tz_localize('Europe/Warsaw', nonexistent='shift_backward')\n        2015-03-29 01:59:59.999999999+01:00    0\n        2015-03-29 03:30:00+02:00              1\n        dtype: int64\n        >>> s.tz_localize('Europe/Warsaw', nonexistent=pd.Timedelta('1H'))\n        2015-03-29 03:30:00+02:00    0\n        2015-03-29 03:30:00+02:00    1\n        dtype: int64\n        "
    nonexistent_options = ('raise', 'NaT', 'shift_forward', 'shift_backward')
    if ((nonexistent not in nonexistent_options) and (not isinstance(nonexistent, timedelta))):
        raise ValueError("The nonexistent argument must be one of 'raise', 'NaT', 'shift_forward', 'shift_backward' or a timedelta object")
    axis = self._get_axis_number(axis)
    ax = self._get_axis(axis)

    def _tz_localize(ax, tz, ambiguous, nonexistent):
        if (not hasattr(ax, 'tz_localize')):
            if (len(ax) > 0):
                ax_name = self._get_axis_name(axis)
                raise TypeError(('%s is not a valid DatetimeIndex or PeriodIndex' % ax_name))
            else:
                ax = DatetimeIndex([], tz=tz)
        else:
            ax = ax.tz_localize(tz, ambiguous=ambiguous, nonexistent=nonexistent)
        return ax
    if isinstance(ax, MultiIndex):
        level = ax._get_level_number(level)
        new_level = _tz_localize(ax.levels[level], tz, ambiguous, nonexistent)
        ax = ax.set_levels(new_level, level=level)
    else:
        if (level not in (None, 0, ax.name)):
            raise ValueError('The level {0} is not valid'.format(level))
        ax = _tz_localize(ax, tz, ambiguous, nonexistent)
    result = self._constructor(self._data, copy=copy)
    result = result.set_axis(ax, axis=axis, inplace=False)
    return result.__finalize__(self)
