def get_service_endpoint(self, service_type):
    if self._endpoints.get(service_type):
        return self._endpoints.get(service_type)
    e = None
    try:
        e = self._session.get_endpoint_data(service_type=service_type, region_name=self.module.params['region'])
    except getattr(requests.exceptions, 'RequestException') as inst:
        self.module.fail_json(msg=inst.message)
    if ((not e) or (e.url == '')):
        self.module.fail_json(msg=('Can not find the enpoint for %s' % service_type))
    url = e.url
    if (url[(- 1)] != '/'):
        url += '/'
    self._endpoints[service_type] = url
    return url