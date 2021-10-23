

def _connect(self):
    api_key = self.module.params.get('api_key')
    api_secret = self.module.params.get('api_secret')
    api_url = self.module.params.get('api_url')
    api_http_method = self.module.params.get('api_http_method')
    api_timeout = self.module.params.get('api_timeout')
    if (api_key and api_secret and api_url):
        self.cs = CloudStack(endpoint=api_url, key=api_key, secret=api_secret, timeout=api_timeout, method=api_http_method)
    else:
        api_region = self.module.params.get('api_region', 'cloudstack')
        self.cs = CloudStack(**read_config(api_region))
