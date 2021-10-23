def W(self):
    'ISO-8601 week number of year, weeks starting on Monday'
    return self.data.isocalendar()[1]