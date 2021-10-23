def _get_server_api_version(self):
    '\n        Fetches the Galaxy API current version to ensure\n        the API server is up and reachable.\n        '
    url = ('%s/api/' % self._api_server)
    try:
        return_data = open_url(url, validate_certs=self._validate_certs)
    except Exception as e:
        raise AnsibleError(('Failed to get data from the API server (%s): %s ' % (url, to_native(e))))
    try:
        data = json.loads(to_text(return_data.read(), errors='surrogate_or_strict'))
    except Exception as e:
        raise AnsibleError(('Could not process data from the API server (%s): %s ' % (url, to_native(e))))
    if ('current_version' not in data):
        raise AnsibleError(("missing required 'current_version' from server response (%s)" % url))
    return data['current_version']