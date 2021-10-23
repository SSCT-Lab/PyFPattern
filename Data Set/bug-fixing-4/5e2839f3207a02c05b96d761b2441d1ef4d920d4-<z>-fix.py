def z(self):
    'Day of the year, i.e. 1 to 366.'
    return self.data.timetuple().tm_yday