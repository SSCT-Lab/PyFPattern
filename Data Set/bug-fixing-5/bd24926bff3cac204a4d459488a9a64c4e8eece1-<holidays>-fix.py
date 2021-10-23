def holidays(self, start=None, end=None, return_name=False):
    '\n        Returns a curve with holidays between start_date and end_date\n\n        Parameters\n        ----------\n        start : starting date, datetime-like, optional\n        end : ending date, datetime-like, optional\n        return_name : bool, optional\n            If True, return a series that has dates and holiday names.\n            False will only return a DatetimeIndex of dates.\n\n        Returns\n        -------\n            DatetimeIndex of holidays\n        '
    if (self.rules is None):
        raise Exception(('Holiday Calendar %s does not have any rules specified' % self.name))
    if (start is None):
        start = AbstractHolidayCalendar.start_date
    if (end is None):
        end = AbstractHolidayCalendar.end_date
    start = Timestamp(start)
    end = Timestamp(end)
    holidays = None
    if ((self._cache is None) or (start < self._cache[0]) or (end > self._cache[1])):
        for rule in self.rules:
            rule_holidays = rule.dates(start, end, return_name=True)
            if (holidays is None):
                holidays = rule_holidays
            else:
                holidays = holidays.append(rule_holidays)
        self._cache = (start, end, holidays.sort_index())
    holidays = self._cache[2]
    holidays = holidays[start:end]
    if return_name:
        return holidays
    else:
        return holidays.index