def exec_module(self, **kwargs):
    'Main module execution method'
    for key in list(self.module_arg_spec.keys()):
        setattr(self, key, kwargs[key])
    resource_group = None
    response = None
    to_be_updated = False
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    if (self.state == 'present'):
        response = self.get_vmextension()
        if (not response):
            to_be_updated = True
        else:
            if (response['settings'] != self.settings):
                response['settings'] = self.settings
                to_be_updated = True
            if (response['protected_settings'] != self.protected_settings):
                response['protected_settings'] = self.protected_settings
                to_be_updated = True
        if to_be_updated:
            self.results['changed'] = True
            self.results['state'] = self.create_or_update_vmextension()
    elif (self.state == 'absent'):
        self.delete_vmextension()
        self.results['changed'] = True
    return self.results