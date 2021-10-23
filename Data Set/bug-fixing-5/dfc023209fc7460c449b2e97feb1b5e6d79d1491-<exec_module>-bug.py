def exec_module(self, **kwargs):
    'Main module execution method'
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    resource_group = None
    response = None
    to_do = Actions.NoAction
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    if (self.state == 'present'):
        response = self.get_containerregistry()
        if (not response):
            to_do = Actions.Create
        else:
            self.log('Results : {0}'.format(response))
            self.results.update(response)
            if (response['provisioning_state'] == 'Succeeded'):
                to_do = Actions.NoAction
                if ((self.location is not None) and (self.location != response['location'])):
                    to_do = Actions.Update
                elif ((self.sku is not None) and (self.location != response['sku'])):
                    to_do = Actions.Update
            else:
                to_do = Actions.NoAction
        self.log('Create / Update the container registry instance')
        if self.check_mode:
            return self.results
        self.results.update(self.create_update_containerregistry(to_do))
        if (to_do != Actions.NoAction):
            self.results['changed'] = True
        else:
            self.results['changed'] = False
        self.log('Container registry instance created or updated')
    elif (self.state == 'absent'):
        if self.check_mode:
            return self.results
        self.delete_containerregistry()
        self.log('Container registry instance deleted')
    return self.results