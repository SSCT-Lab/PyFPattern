def last(self, offset):
    "\n        Method to subset final periods of time series data based on a date offset.\n\n        Parameters\n        ----------\n        offset : str, DateOffset, dateutil.relativedelta\n\n        Returns\n        -------\n        subset : same type as caller\n\n        Raises\n        ------\n        TypeError\n            If the index is not  a :class:`DatetimeIndex`\n\n        See Also\n        --------\n        first : Select initial periods of time series based on a date offset.\n        at_time : Select values at a particular time of the day.\n        between_time : Select values between particular times of the day.\n\n        Examples\n        --------\n        >>> i = pd.date_range('2018-04-09', periods=4, freq='2D')\n        >>> ts = pd.DataFrame({'A': [1, 2, 3, 4]}, index=i)\n        >>> ts\n                    A\n        2018-04-09  1\n        2018-04-11  2\n        2018-04-13  3\n        2018-04-15  4\n\n        Get the rows for the last 3 days:\n\n        >>> ts.last('3D')\n                    A\n        2018-04-13  3\n        2018-04-15  4\n\n        Notice the data for 3 last calender days were returned, not the last\n        3 observed days in the dataset, and therefore data for 2018-04-11 was\n        not returned.\n        "
    if (not isinstance(self.index, DatetimeIndex)):
        raise TypeError("'last' only supports a DatetimeIndex index")
    if (len(self.index) == 0):
        return self
    offset = to_offset(offset)
    start_date = (self.index[(- 1)] - offset)
    start = self.index.searchsorted(start_date, side='right')
    return self.iloc[start:]