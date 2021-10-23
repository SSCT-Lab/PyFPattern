def get_release(self, create=False):
    "Convenient helper to return the release for the current data\n        and optionally creates the release if it's missing.  In case there\n        is no release info it will return `None`.\n        "
    release = self.data.get('release')
    if (not release):
        return None
    if (not create):
        return Release.get(project=self.project, version=self.data['release'])
    timestamp = self.data.get('timestamp')
    if (timestamp is not None):
        date = datetime.fromtimestamp(timestamp)
    else:
        date = None
    return Release.get_or_create(project=self.project, version=self.data['release'], date_added=date)