def execute_module(self):
    changed = False
    results = []
    self.client = self.get_api_client()
    flattened_definitions = []
    for definition in self.resource_definitions:
        kind = definition.get('kind', self.kind)
        api_version = definition.get('apiVersion', self.api_version)
        if kind.endswith('List'):
            resource = self.find_resource(kind, api_version, fail=False)
            flattened_definitions.extend(self.flatten_list_kind(resource, definition))
        else:
            resource = self.find_resource(kind, api_version, fail=True)
            flattened_definitions.append((resource, definition))
    for (resource, definition) in flattened_definitions:
        kind = definition.get('kind', self.kind)
        api_version = definition.get('apiVersion', self.api_version)
        definition = self.set_defaults(resource, definition)
        self.warnings = []
        if (self.params['validate'] is not None):
            self.warnings = self.validate(definition)
        result = self.perform_action(resource, definition)
        result['warnings'] = self.warnings
        changed = (changed or result['changed'])
        results.append(result)
    if (len(results) == 1):
        self.exit_json(**results[0])
    self.exit_json(**{
        'changed': changed,
        'result': {
            'results': results,
        },
    })