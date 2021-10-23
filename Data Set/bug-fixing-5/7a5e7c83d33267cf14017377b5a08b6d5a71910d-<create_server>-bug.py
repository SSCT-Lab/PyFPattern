def create_server(self):
    data = self._module.params.copy()
    missing_parameters = []
    for p in ('name', 'ssh_keys', 'image', 'flavor'):
        if ((p not in data) or (not data[p])):
            missing_parameters.append(p)
    if (len(missing_parameters) > 0):
        self._module.fail_json(msg=('Missing required parameter(s) to create a new server: %s.' % ' '.join(missing_parameters)))
    for (k, v) in data.items():
        if (k in ('api_token', 'api_timeout', 'uuid', 'state')):
            del data[k]
            continue
        if (v is None):
            del data[k]
            continue
    self.info = self._transform_state(self._post('servers', data))
    self.wait_for_state(('running',))