def _fetch_information(self, url):
    response = open_url(url, headers=self.headers, timeout=self.timeout, validate_certs=self.validate_certs)
    try:
        raw_data = to_text(response.read(), errors='surrogate_or_strict')
    except UnicodeError:
        raise AnsibleError('Incorrect encoding of fetched payload from NetBox API.')
    try:
        return json.loads(raw_data)
    except ValueError:
        raise AnsibleError(('Incorrect JSON payload: %s' % raw_data))