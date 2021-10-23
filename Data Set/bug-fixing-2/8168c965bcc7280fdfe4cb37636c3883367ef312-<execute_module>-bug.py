

def execute_module(self):
    ephemeral = self.params.get('ephemeral')
    k8s_state = our_state = self.params.get('state')
    kind = ('VirtualMachineInstance' if ephemeral else 'VirtualMachine')
    _used_params = [name for name in self.params if (self.params[name] is not None)]
    vm_spec_change = (True if set(VM_SPEC_PARAMS).intersection(_used_params) else False)
    changed = False
    crud_executed = False
    method = ''
    if ephemeral:
        if (our_state == 'running'):
            self.params['state'] = k8s_state = 'present'
        elif (our_state == 'stopped'):
            self.params['state'] = k8s_state = 'absent'
    elif (our_state != 'absent'):
        self.params['state'] = k8s_state = 'present'
    self.client = self.get_api_client()
    self._kind_resource = self.find_supported_resource(kind)
    k8s_obj = self.get_resource(self._kind_resource)
    if ((not self.check_mode) and (not vm_spec_change) and (k8s_state != 'absent') and (not k8s_obj)):
        self.fail("It's impossible to create an empty VM or change state of a non-existent VM.")
    if (vm_spec_change or ephemeral or (k8s_state == 'absent') or self.check_mode):
        definition = self.construct_definition(kind, our_state, ephemeral)
        result = self.execute_crud(kind, definition)
        changed = result['changed']
        k8s_obj = result['result']
        method = result['method']
        crud_executed = True
    if (ephemeral and self.params.get('wait') and (k8s_state == 'present') and (not self.check_mode)):
        k8s_obj = self._wait_for_vmi_running()
    if ((not ephemeral) and (our_state in ['running', 'stopped']) and (not self.check_mode)):
        (patched, k8s_obj) = self.manage_vm_state(our_state, crud_executed)
        changed = (changed or patched)
        if changed:
            method = (method or 'patch')
    self.exit_json(**{
        'changed': changed,
        'kubevirt_vm': self.fix_serialization(k8s_obj),
        'method': method,
    })
