def exec_module(self, **kwargs):
    'Main module execution method'
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    resource_group = None
    response = None
    results = dict()
    self.cgmodels = self.containerinstance_client.container_groups.models
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    response = self.get_containerinstance()
    if (not response):
        self.log("Container Group doesn't exist")
        if (self.state == 'absent'):
            self.log('Nothing to delete')
        else:
            self.force_update = True
    else:
        self.log('Container instance already exists')
        if (self.state == 'absent'):
            if (not self.check_mode):
                self.delete_containerinstance()
            self.results['changed'] = True
            self.log('Container instance deleted')
        elif (self.state == 'present'):
            self.log('Need to check if container group has to be deleted or may be updated')
            (update_tags, newtags) = self.update_tags(response.get('tags', dict()))
            if update_tags:
                self.tags = newtags
            if self.force_update:
                self.log('Deleting container instance before update')
                if (not self.check_mode):
                    self.delete_containerinstance()
    if (self.state == 'present'):
        self.log('Need to Create / Update the container instance')
        if self.force_update:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.create_update_containerinstance()
        self.results['id'] = response['id']
        self.results['provisioning_state'] = response['provisioning_state']
        self.results['ip_address'] = response['ip_address']['ip']
        self.log('Creation / Update done')
    return self.results