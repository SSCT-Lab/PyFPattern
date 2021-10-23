

def exec_module(self, **kwargs):
    'Main module execution method'
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    resource_group = None
    to_be_updated = False
    update_tags = False
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    response = self.get_aks()
    if (self.state == 'present'):
        agentpoolcount = len(self.agent_pool_profiles)
        if (agentpoolcount > 1):
            self.fail('You cannot specify more than one agent_pool_profiles currently')
        available_versions = self.get_all_versions()
        if (self.kubernetes_version not in available_versions.keys()):
            self.fail('Unsupported kubernetes version. Excepted one of {0} but get {1}'.format(available_versions.keys(), self.kubernetes_version))
        if (not response):
            to_be_updated = True
        else:
            self.results = response
            self.results['changed'] = False
            self.log('Results : {0}'.format(response))
            (update_tags, response['tags']) = self.update_tags(response['tags'])
            if (response['provisioning_state'] == 'Succeeded'):

                def is_property_changed(profile, property, ignore_case=False):
                    base = response[profile].get(property)
                    new = getattr(self, profile).get(property)
                    if ignore_case:
                        return (base.lower() != new.lower())
                    else:
                        return (base != new)
                if is_property_changed('linux_profile', 'ssh_key'):
                    self.log('Linux Profile Diff SSH, Was {0} / Now {1}'.format(response['linux_profile']['ssh_key'], self.linux_profile.get('ssh_key')))
                    to_be_updated = True
                if is_property_changed('linux_profile', 'admin_username'):
                    self.log('Linux Profile Diff User, Was {0} / Now {1}'.format(response['linux_profile']['admin_username'], self.linux_profile.get('admin_username')))
                    to_be_updated = True
                if (len(response['agent_pool_profiles']) != len(self.agent_pool_profiles)):
                    self.log('Agent Pool count is diff, need to updated')
                    to_be_updated = True
                if (response['kubernetes_version'] != self.kubernetes_version):
                    upgrade_versions = available_versions.get(response['kubernetes_version'])
                    if (upgrade_versions and (self.kubernetes_version not in upgrade_versions)):
                        self.fail('Cannot upgrade kubernetes version to {0}, supported value are {1}'.format(self.kubernetes_version, upgrade_versions))
                    to_be_updated = True
                if (response['enable_rbac'] != self.enable_rbac):
                    to_be_updated = True
                if self.network_profile:
                    for key in self.network_profile.keys():
                        original = (response['network_profile'].get(key) or '')
                        if (self.network_profile[key] and (self.network_profile[key].lower() != original.lower())):
                            to_be_updated = True

                def compare_addon(origin, patch, config):
                    if (not patch):
                        return True
                    if (not origin):
                        return False
                    if (origin['enabled'] != patch['enabled']):
                        return False
                    config = (config or dict())
                    for key in config.keys():
                        if (origin.get(config[key]) != patch.get(key)):
                            return False
                    return True
                if self.addon:
                    for key in ADDONS.keys():
                        addon_name = ADDONS[key]['name']
                        if (not compare_addon(response['addon'].get(addon_name), self.addon.get(key), ADDONS[key].get('config'))):
                            to_be_updated = True
                for profile_result in response['agent_pool_profiles']:
                    matched = False
                    for profile_self in self.agent_pool_profiles:
                        if (profile_result['name'] == profile_self['name']):
                            matched = True
                            os_disk_size_gb = (profile_self.get('os_disk_size_gb') or profile_result['os_disk_size_gb'])
                            if ((profile_result['count'] != profile_self['count']) or (profile_result['vm_size'] != profile_self['vm_size']) or (profile_result['os_disk_size_gb'] != os_disk_size_gb) or (profile_result['vnet_subnet_id'] != profile_self.get('vnet_subnet_id', profile_result['vnet_subnet_id']))):
                                self.log('Agent Profile Diff - Origin {0} / Update {1}'.format(str(profile_result), str(profile_self)))
                                to_be_updated = True
                    if (not matched):
                        self.log('Agent Pool not found')
                        to_be_updated = True
        if to_be_updated:
            self.log('Need to Create / Update the AKS instance')
            if (not self.check_mode):
                self.results = self.create_update_aks()
                self.log('Creation / Update done')
            self.results['changed'] = True
        elif update_tags:
            self.log('Need to Update the AKS tags')
            if (not self.check_mode):
                self.results['tags'] = self.update_aks_tags()
            self.results['changed'] = True
        return self.results
    elif ((self.state == 'absent') and response):
        self.log('Need to Delete the AKS instance')
        self.results['changed'] = True
        if self.check_mode:
            return self.results
        self.delete_aks()
        self.log('AKS instance deleted')
    return self.results
