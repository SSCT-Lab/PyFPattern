def execute_module(self):
    changed = False
    results = []
    self.client = self.get_api_client()
    for definition in self.resource_definitions:
        kind = definition.get('kind')
        search_kind = kind
        if kind.lower().endswith('list'):
            search_kind = kind[:(- 4)]
        api_version = definition.get('apiVersion')
        resource = self.find_resource(search_kind, api_version, fail=True)
        definition['kind'] = resource.kind
        definition['apiVersion'] = resource.group_version
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