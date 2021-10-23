def get_metadata(self):
    exception = self.data['sentry.interfaces.Exception']['values'][0]
    return {
        'type': exception.get('type', 'Error'),
        'value': exception.get('value', ''),
    }