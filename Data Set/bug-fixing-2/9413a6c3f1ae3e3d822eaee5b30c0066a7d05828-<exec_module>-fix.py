

def exec_module(self, **kwargs):
    for key in self.module_arg_spec:
        setattr(self, key, kwargs[key])
    self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient, base_url=self._cloud_environment.endpoints.resource_manager)
    if (self.url is None):
        orphan = None
        rargs = dict()
        rargs['subscription'] = self.subscription_id
        rargs['resource_group'] = self.resource_group
        if (not ((self.provider is None) or self.provider.lower().startswith('.microsoft'))):
            rargs['namespace'] = ('Microsoft.' + self.provider)
        else:
            rargs['namespace'] = self.provider
        if ((self.resource_type is not None) and (self.resource_name is not None)):
            rargs['type'] = self.resource_type
            rargs['name'] = self.resource_name
            for i in range(len(self.subresource)):
                resource_ns = self.subresource[i].get('namespace', None)
                resource_type = self.subresource[i].get('type', None)
                resource_name = self.subresource[i].get('name', None)
                if ((resource_type is not None) and (resource_name is not None)):
                    rargs[('child_namespace_' + str((i + 1)))] = resource_ns
                    rargs[('child_type_' + str((i + 1)))] = resource_type
                    rargs[('child_name_' + str((i + 1)))] = resource_name
                else:
                    orphan = resource_type
        else:
            orphan = self.resource_type
        self.url = resource_id(**rargs)
        if (orphan is not None):
            self.url += ('/' + orphan)
    self.results['url'] = self.url
    query_parameters = {
        
    }
    query_parameters['api-version'] = self.api_version
    header_parameters = {
        
    }
    header_parameters['Content-Type'] = 'application/json; charset=utf-8'
    skiptoken = None
    while True:
        if skiptoken:
            query_parameters['skiptoken'] = skiptoken
        response = self.mgmt_client.query(self.url, 'GET', query_parameters, header_parameters, None, [200, 404], 0, 0)
        try:
            response = json.loads(response.text)
            if isinstance(response, dict):
                if response.get('value'):
                    self.results['response'] = (self.results['response'] + response['value'])
                    skiptoken = response.get('nextLink')
                else:
                    self.results['response'] = (self.results['response'] + [response])
        except Exception:
            self.results['response'] = []
        if (not skiptoken):
            break
    return self.results
