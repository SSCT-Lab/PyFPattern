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
            if (self.settings is not None):
                if (response['settings'] != self.settings):
                    response['settings'] = self.settings
                    to_be_updated = True
            else:
                self.settings = response['settings']
            if (self.protected_settings is not None):
                if (response['protected_settings'] != self.protected_settings):
                    response['protected_settings'] = self.protected_settings
                    to_be_updated = True
            else:
                self.protected_settings = response['protected_settings']
            if (response['location'] != self.location):
                self.location = response['location']
                self.module.warn("Property 'location' cannot be changed")
            if (response['publisher'] != self.publisher):
                self.publisher = response['publisher']
                self.module.warn("Property 'publisher' cannot be changed")
            if (response['virtual_machine_extension_type'] != self.virtual_machine_extension_type):
                self.virtual_machine_extension_type = response['virtual_machine_extension_type']
                self.module.warn("Property 'virtual_machine_extension_type' cannot be changed")
            if (response['type_handler_version'] != self.type_handler_version):
                response['type_handler_version'] = self.type_handler_version
                to_be_updated = True
            if (self.auto_upgrade_minor_version is not None):
                if (response['auto_upgrade_minor_version'] != self.auto_upgrade_minor_version):
                    response['auto_upgrade_minor_version'] = self.auto_upgrade_minor_version
                    to_be_updated = True
            else:
                self.auto_upgrade_minor_version = response['auto_upgrade_minor_version']
        if to_be_updated:
            self.results['changed'] = True
            self.results['state'] = self.create_or_update_vmextension()
    elif (self.state == 'absent'):
        self.delete_vmextension()
        self.results['changed'] = True
    return self.results