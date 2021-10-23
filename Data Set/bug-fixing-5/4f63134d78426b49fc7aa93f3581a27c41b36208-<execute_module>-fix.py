def execute_module(self):
    changed = False
    results = []
    self.client = self.get_api_client()
    for definition in self.resource_definitions:
        kind = definition.get('kind', self.kind)
        search_kind = kind
        if kind.lower().endswith('list'):
            search_kind = kind[:(- 4)]
        api_version = definition.get('apiVersion', self.api_version)
        resource = self.find_resource(search_kind, api_version, fail=True)
        definition = self.set_defaults(resource, definition)
        result = self.perform_action(resource, definition)
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