def _fetch(self, url):
    (response, info) = fetch_url(self.module, url, force=True)
    if response:
        data = response.read()
    else:
        data = None
    return data