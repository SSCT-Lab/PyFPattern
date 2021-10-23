def exec_module(self, **kwargs):
    'Main module execution method'
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    resource_group = None
    response = None
    results = dict()
    to_be_updated = False
    try:
        resource_group = self.get_resource_group(self.resource_group)
    except CloudError:
        self.fail('resource group {} not found'.format(self.resource_group))
    if (not self.location):
        self.location = resource_group.location
    if (self.state == 'present'):
        if (self.orchestration_platform == 'Kubernetes'):
            if (not self.service_principal):
                self.fail('service_principal should be specified when using Kubernetes')
            if (not self.service_principal[0].get('client_id')):
                self.fail('service_principal.client_id should be specified when using Kubernetes')
            if (not self.service_principal[0].get('client_secret')):
                self.fail('service_principal.client_secret should be specified when using Kubernetes')
        mastercount = self.master_profile[0].get('count')
        if ((mastercount != 1) and (mastercount != 3) and (mastercount != 5)):
            self.fail('Master Count number wrong : {} / should be 1 3 or 5'.format(mastercount))
        agentpoolcount = len(self.agent_pool_profiles)
        if (agentpoolcount > 1):
            self.fail('You cannot specify more than agent_pool_profiles')
        response = self.get_acs()
        self.results['state'] = response
        if (not response):
            to_be_updated = True
        else:
            self.log('Results : {0}'.format(response))
            (update_tags, response['tags']) = self.update_tags(response['tags'])
            if (response['provisioning_state'] == 'Succeeded'):
                if update_tags:
                    to_be_updated = True
                if (response['master_profile'].get('count') != self.master_profile[0].get('count')):
                    self.module.warn('master_profile.count cannot be updated')
                if (response['linux_profile'].get('ssh_key') != self.linux_profile[0].get('ssh_key')):
                    self.module.warn('linux_profile.ssh_key cannot be updated')
                if (response['linux_profile'].get('admin_username') != self.linux_profile[0].get('admin_username')):
                    self.module.warn('linux_profile.admin_username cannot be updated')
                for profile_result in response['agent_pool_profiles']:
                    matched = False
                    for profile_self in self.agent_pool_profiles:
                        if (profile_result['name'] == profile_self['name']):
                            matched = True
                            if ((profile_result['count'] != profile_self['count']) or (profile_result['vm_size'] != profile_self['vm_size'])):
                                self.log('Agent Profile Diff - Count was {0} / Now {1} - Vm_size was {2} / Now {3}'.format(profile_result['count'], profile_self['count'], profile_result['vm_size'], profile_self['vm_size']))
                                to_be_updated = True
                    if (not matched):
                        self.log('Agent Pool not found')
                        to_be_updated = True
        if to_be_updated:
            self.log('Need to Create / Update the ACS instance')
            if self.check_mode:
                return self.results
            self.results['state'] = self.create_update_acs()
            self.results['changed'] = True
            self.log('Creation / Update done')
    elif (self.state == 'absent'):
        self.delete_acs()
        self.log('ACS instance deleted')
    return self.results