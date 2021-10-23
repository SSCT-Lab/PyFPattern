def refresh_url(self):
    query_parameters = [('limit', 0)]
    if self.query_filters:
        query_parameters.extend(filter((lambda x: x), map(self.validate_query_parameters, self.query_filters)))
    if self.config_context:
        self.device_url = ((self.api_endpoint + '/api/dcim/devices/?') + urlencode(query_parameters))
        self.virtual_machines_url = ((self.api_endpoint + '/api/virtualization/virtual-machines/?') + urlencode(query_parameters))
    else:
        self.device_url = (((self.api_endpoint + '/api/dcim/devices/?') + urlencode(query_parameters)) + '&exclude=config_context')
        self.virtual_machines_url = (((self.api_endpoint + '/api/virtualization/virtual-machines/?') + urlencode(query_parameters)) + '&exclude=config_context')