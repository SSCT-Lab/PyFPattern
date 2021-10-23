@property
def build_date(self):
    'Normalizes the build_date string\n\n        The ISOs usually ship with a broken format\n\n        ex: Tue May 15 15 26 30 PDT 2018\n\n        This will re-format that time so that it looks like ISO 8601 without\n        microseconds\n\n        ex: 2018-05-15T15:26:30\n\n        :return:\n        '
    if (self._values['build_date'] is None):
        return None
    result = datetime.datetime.strptime(self._values['build_date'], '%a %b %d %H %M %S PDT %Y').isoformat()
    return result