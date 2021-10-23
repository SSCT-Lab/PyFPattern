

def execute_module(self):
    definition = virtdict()
    kind = 'Template'
    definition['parameters'] = self.params.get('parameters')
    annotations = definition['metadata']['annotations']
    if self.params.get('display_name'):
        annotations['openshift.io/display-name'] = self.params.get('display_name')
    if self.params.get('description'):
        annotations['description'] = self.params.get('description')
    if self.params.get('long_description'):
        annotations['openshift.io/long-description'] = self.params.get('long_description')
    if self.params.get('provider_display_name'):
        annotations['openshift.io/provider-display-name'] = self.params.get('provider_display_name')
    if self.params.get('documentation_url'):
        annotations['openshift.io/documentation-url'] = self.params.get('documentation_url')
    if self.params.get('support_url'):
        annotations['openshift.io/support-url'] = self.params.get('support_url')
    if self.params.get('icon_class'):
        annotations['iconClass'] = self.params.get('icon_class')
    if self.params.get('version'):
        annotations['template.cnv.io/version'] = self.params.get('version')
    if self.params.get('editable'):
        annotations['template.cnv.io/editable'] = self.params.get('editable')
    if self.params.get('default_disk'):
        annotations['defaults.template.cnv.io/disk'] = self.params.get('default_disk').get('name')
    if self.params.get('default_volume'):
        annotations['defaults.template.cnv.io/volume'] = self.params.get('default_volume').get('name')
    if self.params.get('default_nic'):
        annotations['defaults.template.cnv.io/nic'] = self.params.get('default_nic').get('name')
    if self.params.get('default_network'):
        annotations['defaults.template.cnv.io/network'] = self.params.get('default_network').get('name')
    self.client = self.get_api_client()
    definition['objects'] = []
    objects = (self.params.get('objects') or [])
    for obj in objects:
        if (obj['kind'] != 'VirtualMachine'):
            definition['objects'].append(obj)
        else:
            vm_definition = virtdict()
            if self.params.get('default_disk'):
                vm_definition['spec']['template']['spec']['domain']['devices']['disks'] = [self.params.get('default_disk')]
            if self.params.get('default_volume'):
                vm_definition['spec']['template']['spec']['volumes'] = [self.params.get('default_volume')]
            if self.params.get('default_nic'):
                vm_definition['spec']['template']['spec']['domain']['devices']['interfaces'] = [self.params.get('default_nic')]
            if self.params.get('default_network'):
                vm_definition['spec']['template']['spec']['networks'] = [self.params.get('default_network')]
            vm_definition['apiVersion'] = MAX_SUPPORTED_API_VERSION
            vm_template = vm_definition['spec']['template']
            (dummy, vm_def) = self.construct_vm_template_definition('VirtualMachine', vm_definition, vm_template, obj)
            definition['objects'].append(vm_def)
    result = self.execute_crud(kind, definition)
    self.exit_json(**{
        'changed': result['changed'],
        'kubevirt_template': result.pop('result'),
        'result': result,
    })
