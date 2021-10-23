def z(self):
    'Day of the year, i.e. 1 to 366.'
    doy = (self.year_days[self.data.month] + self.data.day)
    if (self.L() and (self.data.month > 2)):
        doy += 1
    return doy