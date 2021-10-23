def _verify_timezone(self):
    tz = self.value['name']['planned']
    tzfile = ('/usr/share/zoneinfo/%s' % tz)
    if (not os.path.isfile(tzfile)):
        self.abort(('given timezone "%s" is not available' % tz))