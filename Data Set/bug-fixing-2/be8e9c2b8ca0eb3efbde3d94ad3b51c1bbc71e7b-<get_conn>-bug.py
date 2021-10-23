

def get_conn(self, version='v1'):
    '\n        Returns a Google Cloud Storage service object.\n        '
    http_authorized = self._authorize()
    return build('datastore', version, http=http_authorized, cache_discovery=False)
