def execute_module(self):
    KIND = 'PersistentVolumeClaim'
    API = 'v1'
    definition = virtdict()
    definition['kind'] = KIND
    definition['apiVersion'] = API
    metadata = definition['metadata']
    metadata['name'] = self.params.get('name')
    metadata['namespace'] = self.params.get('namespace')
    if self.params.get('annotations'):
        metadata['annotations'] = self.params.get('annotations')
    if self.params.get('labels'):
        metadata['labels'] = self.params.get('labels')
    if self.params.get('cdi_source'):
        self._parse_cdi_source(self.params.get('cdi_source'), metadata)
    spec = definition['spec']
    if self.params.get('access_modes'):
        spec['accessModes'] = self.params.get('access_modes')
    if self.params.get('size'):
        spec['resources']['requests']['storage'] = self.params.get('size')
    if self.params.get('storage_class_name'):
        spec['storageClassName'] = self.params.get('storage_class_name')
    if self.params.get('selector'):
        spec['selector'] = self.params.get('selector')
    if self.params.get('volume_mode'):
        spec['volumeMode'] = self.params.get('volume_mode')
    if self.params.get('volume_name'):
        spec['volumeName'] = self.params.get('volume_name')
    definition = dict(KubeVirtRawModule.merge_dicts(self.resource_definitions[0], definition))
    self.client = self.get_api_client()
    resource = self.find_resource(KIND, API, fail=True)
    definition = self.set_defaults(resource, definition)
    result = self.perform_action(resource, definition)
    if (self.params.get('wait') and (self.params.get('state') == 'present')):
        result['result'] = self._wait_for_creation(resource, result['result'])
    self.exit_json(**result)