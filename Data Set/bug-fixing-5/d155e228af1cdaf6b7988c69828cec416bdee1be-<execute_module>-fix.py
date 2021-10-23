def execute_module(self):
    definition = virtdict()
    ephemeral = self.params.get('ephemeral')
    state = self.params.get('state')
    if (not ephemeral):
        definition['spec']['running'] = (state == 'running')
    template = (definition if ephemeral else definition['spec']['template'])
    kind = ('VirtualMachineInstance' if ephemeral else 'VirtualMachine')
    (dummy, definition) = self.construct_vm_definition(kind, definition, template)
    result = self.execute_crud(kind, definition)
    changed = result['changed']
    if (state in ['running', 'stopped']):
        if (not self.check_mode):
            ret = self.manage_state(state)
            changed = (changed or ret)
    self.exit_json(**{
        'changed': changed,
        'kubevirt_vm': result.pop('result'),
        'result': result,
    })