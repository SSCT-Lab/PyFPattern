def exec_module(self, **kwargs):
    'Main module execution method'
    for key in list(self.module_arg_spec.keys()):
        setattr(self, key, kwargs[key])
    to_be_updated = False
    resource_group = self.get_resource_group(self.resource_group)
    self.virtual_network = self.parse_resource_to_dict(self.virtual_network)
    if (self.virtual_network['resource_group'] != self.resource_group):
        self.fail('Resource group of virtual_network is not same as param resource_group')
    self.remote_virtual_network = self.parse_resource_to_dict(self.remote_virtual_network)
    response = self.get_vnet_peering()
    if (self.state == 'present'):
        if response:
            existing_vnet = self.parse_resource_to_dict(response['id'])
            if ((existing_vnet['resource_group'] != self.virtual_network['resource_group']) or (existing_vnet['name'] != self.virtual_network['name'])):
                self.fail('Cannot update virtual_network of Virtual Network Peering!')
            exisiting_remote_vnet = self.parse_resource_to_dict(response['remote_virtual_network'])
            if ((exisiting_remote_vnet['resource_group'] != self.remote_virtual_network['resource_group']) or (exisiting_remote_vnet['name'] != self.remote_virtual_network['name'])):
                self.fail('Cannot update remote_virtual_network of Virtual Network Peering!')
            to_be_updated = self.check_update(response)
        else:
            to_be_updated = True
            virtual_network = self.get_vnet(self.virtual_network['resource_group'], self.virtual_network['name'])
            if (not virtual_network):
                self.fail('Virtual network {0} in resource group {1} does not exist!'.format(self.virtual_network['name'], self.virtual_network['resource_group']))
            remote_virtual_network = self.get_vnet(self.remote_virtual_network['resource_group'], self.remote_virtual_network['name'])
            if (not remote_virtual_network):
                self.fail('Virtual network {0} in resource group {1} does not exist!'.format(self.remote_virtual_network['name'], self.remote_virtual_network['resource_group']))
    elif (self.state == 'absent'):
        if response:
            self.log('Delete Azure Virtual Network Peering')
            self.results['changed'] = True
            self.results['id'] = response['id']
            if self.check_mode:
                return self.results
            response = self.delete_vnet_peering()
        else:
            self.fail('Azure Virtual Network Peering {0} does not exist in resource group {1}'.format(self.name, self.resource_group))
    if to_be_updated:
        self.results['changed'] = True
        if self.check_mode:
            return self.results
        response = self.create_or_update_vnet_peering()
        self.results['id'] = response['id']
    return self.results