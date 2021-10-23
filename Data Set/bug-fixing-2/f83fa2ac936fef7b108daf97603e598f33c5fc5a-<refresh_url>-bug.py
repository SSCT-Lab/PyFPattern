

def refresh_url(self):
    query_parameters = [('limit', 0)]
    query_parameters.extend(filter((lambda x: x), map(self.validate_query_parameters, self.query_filters)))
    self.device_url = (((self.api_endpoint + '/api/dcim/devices/') + '?') + urlencode(query_parameters))
    self.virtual_machines_url = ''.join([self.api_endpoint, '/api/virtualization/virtual-machines/', '?', urlencode(query_parameters)])
