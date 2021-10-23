def _validate_freq(self):
    ' validate & return our freq '
    from pandas.tseries.frequencies import to_offset
    try:
        return to_offset(self.window)
    except (TypeError, ValueError):
        raise ValueError('passed window {0} in not compat with a datetimelike index'.format(self.window))