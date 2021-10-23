def W(self):
    'ISO-8601 week number of year, weeks starting on Monday'
    jan1_weekday = (self.data.replace(month=1, day=1).weekday() + 1)
    weekday = (self.data.weekday() + 1)
    day_of_year = self.z()
    if ((day_of_year <= (8 - jan1_weekday)) and (jan1_weekday > 4)):
        if ((jan1_weekday == 5) or ((jan1_weekday == 6) and calendar.isleap((self.data.year - 1)))):
            week_number = 53
        else:
            week_number = 52
    else:
        if calendar.isleap(self.data.year):
            i = 366
        else:
            i = 365
        if ((i - day_of_year) < (4 - weekday)):
            week_number = 1
        else:
            j = ((day_of_year + (7 - weekday)) + (jan1_weekday - 1))
            week_number = (j // 7)
            if (jan1_weekday > 4):
                week_number -= 1
    return week_number