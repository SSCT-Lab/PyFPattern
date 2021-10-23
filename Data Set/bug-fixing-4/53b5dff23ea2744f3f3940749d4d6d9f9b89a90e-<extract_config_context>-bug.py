def extract_config_context(self, host):
    try:
        if self.config_context:
            url = urljoin(self.api_endpoint, ('/api/dcim/devices/' + str(host['id'])))
            device_lookup = self._fetch_information(url)
            return [device_lookup['config_context']]
    except Exception:
        return