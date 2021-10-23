def _fetch(self, path):
    api_ip = self._get_api_ip()
    if (not api_ip):
        return None
    api_url = (path % api_ip)
    (response, info) = fetch_url(module, api_url, force=True)
    if response:
        data = response.read()
    else:
        data = None
    return data