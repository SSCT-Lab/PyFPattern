def _get(self, endpoint, **kwargs):
    ' Perform a GET request on a given API endpoint.\n\n        Automatically extracts result data from the response and converts HTTP\n        exceptions into :py:class:`BeatportAPIError` objects.\n        '
    try:
        response = self.api.get(self._make_url(endpoint), params=kwargs)
    except Exception as e:
        raise BeatportAPIError('Error connecting to Beatport API: {}'.format(e.message))
    if (not response):
        raise BeatportAPIError("Error {0.status_code} for '{0.request.path_url}".format(response))
    return response.json()['results']