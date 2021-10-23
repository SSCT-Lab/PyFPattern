def execute_module(self):
    self.client = self.get_api_client()
    definition = virtdict()
    ephemeral = self.params.get('ephemeral')
    state = self.params.get('state')
    if (not ephemeral):
        definition['spec']['running'] = (state == 'running')
    vm_template = self.params.get('template')
    processedtemplate = {
        
    }
    if vm_template:
        template_resource = self.client.resources.get(api_version='template.openshift.io/v1', kind='Template', name='templates')
        proccess_template = template_resource.get(name=vm_template, namespace=self.params.get('namespace'))
        for (k, v) in self.params.get('parameters', {
            
        }).items():
            for parameter in proccess_template.parameters:
                if (parameter.name == k):
                    parameter.value = v
        processedtemplates_res = self.client.resources.get(api_version='template.openshift.io/v1', kind='Template', name='processedtemplates')
        processedtemplate = processedtemplates_res.create(proccess_template.to_dict()).to_dict()['objects'][0]
    template = (definition if ephemeral else definition['spec']['template'])
    kind = ('VirtualMachineInstance' if ephemeral else 'VirtualMachine')
    template['labels']['vm.cnv.io/name'] = self.params.get('name')
    (dummy, definition) = self.construct_vm_definition(kind, definition, template)
    definition = dict(self.merge_dicts(processedtemplate, definition))
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