def __init__(self, *args, **kwargs):
    self.client = None
    mutually_exclusive = [('resource_definition', 'src')]
    KubernetesAnsibleModule.__init__(self, *args, mutually_exclusive=mutually_exclusive, supports_check_mode=True, **kwargs)
    self.kind = self.params.pop('kind')
    self.api_version = self.params.pop('api_version')
    self.name = self.params.pop('name')
    self.namespace = self.params.pop('namespace')
    resource_definition = self.params.pop('resource_definition')
    if resource_definition:
        if isinstance(resource_definition, string_types):
            try:
                self.resource_definitions = yaml.safe_load_all(resource_definition)
            except (IOError, yaml.YAMLError) as exc:
                self.fail(msg='Error loading resource_definition: {0}'.format(exc))
        elif isinstance(resource_definition, list):
            self.resource_definitions = resource_definition
        else:
            self.resource_definitions = [resource_definition]
    src = self.params.pop('src')
    if src:
        self.resource_definitions = self.load_resource_definitions(src)
    if ((not resource_definition) and (not src)):
        self.resource_definitions = [{
            'kind': self.kind,
            'apiVersion': self.api_version,
            'metadata': {
                'name': self.name,
                'namespace': self.namespace,
            },
        }]