

def __init__(self, k8s_kind=None, *args, **kwargs):
    self.client = None
    self.warnings = []
    mutually_exclusive = [('resource_definition', 'src')]
    KubernetesAnsibleModule.__init__(self, *args, mutually_exclusive=mutually_exclusive, supports_check_mode=True, **kwargs)
    self.kind = (k8s_kind or self.params.get('kind'))
    self.api_version = self.params.get('api_version')
    self.name = self.params.get('name')
    self.namespace = self.params.get('namespace')
    resource_definition = self.params.get('resource_definition')
    validate = self.params.get('validate')
    if validate:
        if (LooseVersion(self.openshift_version) < LooseVersion('0.8.0')):
            self.fail_json(msg='openshift >= 0.8.0 is required for validate')
    self.append_hash = self.params.get('append_hash')
    if self.append_hash:
        if (not HAS_K8S_CONFIG_HASH):
            self.fail_json(msg='openshift >= 0.7.2 is required for append_hash')
    if self.params['merge_type']:
        if (LooseVersion(self.openshift_version) < LooseVersion('0.6.2')):
            self.fail_json(msg='openshift >= 0.6.2 is required for merge_type')
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
    src = self.params.get('src')
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
