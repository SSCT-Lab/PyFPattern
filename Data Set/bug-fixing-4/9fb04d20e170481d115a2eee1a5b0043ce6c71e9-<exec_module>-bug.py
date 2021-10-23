def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['tags']):
        setattr(self, key, kwargs[key])
    results = None
    changed = False
    nic = None
    nsg = None
    resource_group = self.get_resource_group(self.resource_group)
    if (not self.location):
        self.location = resource_group.location
    virtual_network_dict = parse_resource_id(self.virtual_network_name)
    virtual_network_name = virtual_network_dict.get('name')
    virtual_network_resource_group = virtual_network_dict.get('resource_group', self.resource_group)
    if ((self.state == 'present') and (not self.ip_configurations)):
        self.deprecate('Setting ip_configuration flatten is deprecated and will be removed. Using ip_configurations list to define the ip configuration', version='2.9')
        self.ip_configurations = [dict(private_ip_address=self.private_ip_address, private_ip_allocation_method=self.private_ip_allocation_method, public_ip_address_name=(self.public_ip_address_name if self.public_ip else None), public_ip_allocation_method=self.public_ip_allocation_method, name='default')]
    try:
        self.log('Fetching network interface {0}'.format(self.name))
        nic = self.network_client.network_interfaces.get(self.resource_group, self.name)
        self.log('Network interface {0} exists'.format(self.name))
        self.check_provisioning_state(nic, self.state)
        results = nic_to_dict(nic)
        self.log(results, pretty_print=True)
        nsg = None
        if (self.state == 'present'):
            (update_tags, results['tags']) = self.update_tags(results['tags'])
            if update_tags:
                changed = True
            if self.security_group_name:
                nsg = self.get_security_group(self.security_group_name)
                if (nsg and (results['network_security_group'].get('id') != nsg.id)):
                    self.log('CHANGED: network interface {0} network security group'.format(self.name))
                    changed = True
            if (results['ip_configurations'][0]['subnet']['virtual_network_name'] != virtual_network_name):
                self.log('CHANGED: network interface {0} virtual network name'.format(self.name))
                changed = True
            if (results['ip_configurations'][0]['subnet']['resource_group'] != virtual_network_resource_group):
                self.log('CHANGED: network interface {0} virtual network resource group'.format(self.name))
                changed = True
            if (results['ip_configurations'][0]['subnet']['name'] != self.subnet_name):
                self.log('CHANGED: network interface {0} subnet name'.format(self.name))
                changed = True
            ip_configuration_result = construct_ip_configuration_set(results['ip_configurations'])
            ip_configuration_request = construct_ip_configuration_set(self.ip_configurations)
            if (ip_configuration_result != ip_configuration_request):
                self.log('CHANGED: network interface {0} ip configurations'.format(self.name))
                changed = True
        elif (self.state == 'absent'):
            self.log("CHANGED: network interface {0} exists but requested state is 'absent'".format(self.name))
            changed = True
    except CloudError:
        self.log('Network interface {0} does not exist'.format(self.name))
        if (self.state == 'present'):
            self.log("CHANGED: network interface {0} does not exist but requested state is 'present'".format(self.name))
            changed = True
    self.results['changed'] = changed
    self.results['state'] = results
    if self.check_mode:
        return self.results
    if changed:
        if (self.state == 'present'):
            subnet = self.get_subnet(virtual_network_resource_group, virtual_network_name, self.subnet_name)
            if (not subnet):
                self.fail('subnet {0} is not exist'.format(self.subnet_name))
            nic_ip_configurations = [self.network_models.NetworkInterfaceIPConfiguration(private_ip_allocation_method=ip_config.get('private_ip_allocation_method'), private_ip_address=ip_config.get('private_ip_address'), name=ip_config.get('name'), subnet=subnet, public_ip_address=self.get_or_create_public_ip_address(ip_config), primary=ip_config.get('primary')) for ip_config in self.ip_configurations]
            nsg = (nsg or self.create_default_securitygroup(self.resource_group, self.location, self.name, self.os_type, self.open_ports))
            self.log('Creating or updating network interface {0}'.format(self.name))
            nic = self.network_models.NetworkInterface(id=(results['id'] if results else None), location=self.location, tags=self.tags, ip_configurations=nic_ip_configurations, network_security_group=nsg)
            self.results['state'] = self.create_or_update_nic(nic)
        elif (self.state == 'absent'):
            self.log('Deleting network interface {0}'.format(self.name))
            self.delete_nic()
            self.results['state']['status'] = 'Deleted'
    return self.results