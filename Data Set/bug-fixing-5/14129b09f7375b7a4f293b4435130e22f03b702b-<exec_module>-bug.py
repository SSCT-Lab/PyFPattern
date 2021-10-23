def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    results = dict()
    changed = False
    rg = None
    contains_resources = False
    try:
        self.log('Fetching resource group {0}'.format(self.name))
        rg = self.rm_client.resource_groups.get(self.name)
        self.check_provisioning_state(rg, self.state)
        contains_resources = self.resources_exist()
        results = resource_group_to_dict(rg)
        if (self.state == 'absent'):
            self.log("CHANGED: resource group {0} exists but requested state is 'absent'".format(self.name))
            changed = True
        elif (self.state == 'present'):
            (update_tags, results['tags']) = self.update_tags(results['tags'])
            self.log(('update tags %s' % update_tags))
            self.log(('new tags: %s' % str(results['tags'])))
            if update_tags:
                changed = True
            if (self.location and (normalize_location_name(self.location) != results['location'])):
                self.fail("Resource group '{0}' already exists in location '{1}' and cannot be moved.".format(self.name, results['location']))
    except CloudError:
        self.log('Resource group {0} does not exist'.format(self.name))
        if (self.state == 'present'):
            self.log("CHANGED: resource group {0} does not exist but requested state is 'present'".format(self.name))
            changed = True
    self.results['changed'] = changed
    self.results['state'] = results
    self.results['contains_resources'] = contains_resources
    if self.check_mode:
        return self.results
    if changed:
        if (self.state == 'present'):
            if (not rg):
                self.log('Creating resource group {0}'.format(self.name))
                if (not self.location):
                    self.fail('Parameter error: location is required when creating a resource group.')
                if self.name_exists():
                    self.fail('Error: a resource group with the name {0} already exists in your subscription.'.format(self.name))
                params = self.rm_models.ResourceGroup(location=self.location, tags=self.tags)
            else:
                params = self.rm_models.ResourceGroup(location=results['location'], tags=results['tags'])
            self.results['state'] = self.create_or_update_resource_group(params)
        elif (self.state == 'absent'):
            if (contains_resources and (not self.force)):
                self.fail('Error removing resource group {0}. Resources exist within the group.'.format(self.name))
            self.delete_resource_group()
    return self.results