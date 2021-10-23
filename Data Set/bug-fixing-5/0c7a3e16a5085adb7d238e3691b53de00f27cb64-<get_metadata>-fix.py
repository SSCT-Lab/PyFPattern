def get_metadata(self):
    exception = self.data['sentry.interfaces.Exception']['values'][0]
    return {
        'type': trim(exception.get('type', 'Error'), 128),
        'value': trim(exception.get('value', ''), 1024),
    }