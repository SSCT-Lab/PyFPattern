def run(self, terms, variables=None, **kwargs):
    self.kind = kwargs.get('kind')
    self.name = kwargs.get('resource_name')
    self.namespace = kwargs.get('namespace')
    self.api_version = kwargs.get('api_version', 'v1')
    self.label_selector = kwargs.get('label_selector')
    self.field_selector = kwargs.get('field_selector')
    self.include_uninitialized = kwargs.get('include_uninitialized', False)
    resource_definition = kwargs.get('resource_definition')
    src = kwargs.get('src')
    if src:
        resource_definition = self.load_resource_definition(src)
    if resource_definition:
        self.params_from_resource_definition(resource_definition)
    if (not self.kind):
        raise Exception("Error: no Kind specified. Use the 'kind' parameter, or provide an object YAML configuration using the 'resource_definition' parameter.")
    self.kind = to_snake(self.kind)
    self.helper = self.get_helper(self.api_version, self.kind)
    auth_args = ('host', 'api_key', 'kubeconfig', 'context', 'username', 'password', 'cert_file', 'key_file', 'ssl_ca_cert', 'verify_ssl')
    for arg in AUTH_ARG_SPEC:
        if ((arg in auth_args) and (kwargs.get(arg) is not None)):
            self.connection[arg] = kwargs.get(arg)
    try:
        self.helper.set_client_config(**self.connection)
    except Exception as exc:
        raise Exception('Client authentication failed: {0}'.format(exc.message))
    if self.name:
        return self.get_object()
    return self.list_objects()