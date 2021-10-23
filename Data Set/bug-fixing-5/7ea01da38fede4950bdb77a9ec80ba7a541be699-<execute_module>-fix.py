def execute_module(self):
    definition = virtdict()
    selector = self.params.get('selector')
    replicas = self.params.get('replicas')
    if selector:
        definition['spec']['selector'] = selector
    if (replicas is not None):
        definition['spec']['replicas'] = replicas
    template = definition['spec']['template']
    (dummy, definition) = self.construct_vm_definition(KIND, definition, template)
    result_crud = self.execute_crud(KIND, definition)
    changed = result_crud['changed']
    result = result_crud.pop('result')
    if (changed and (result_crud['method'] == 'create') and (replicas is None)):
        replicas = 1
    if (self.params.get('wait') and (replicas is not None) and (self.params.get('state') == 'present')):
        result = self.wait_for_replicas(replicas)
    self.exit_json(**{
        'changed': changed,
        'kubevirt_rs': result,
        'result': result_crud,
    })