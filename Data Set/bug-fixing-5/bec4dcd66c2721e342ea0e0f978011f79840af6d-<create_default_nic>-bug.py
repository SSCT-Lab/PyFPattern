def create_default_nic(self):
    '\n        Create a default Network Interface <vm name>01. Requires an existing virtual network\n        with one subnet. If NIC <vm name>01 exists, use it. Otherwise, create one.\n\n        :return: NIC object\n        '
    network_interface_name = (self.name + '01')
    nic = None
    self.log('Create default NIC {0}'.format(network_interface_name))
    self.log('Check to see if NIC {0} exists'.format(network_interface_name))
    try:
        nic = self.network_client.network_interfaces.get(self.resource_group, network_interface_name)
    except CloudError:
        pass
    if nic:
        self.log('NIC {0} found.'.format(network_interface_name))
        self.check_provisioning_state(nic)
        return nic
    self.log('NIC {0} does not exist.'.format(network_interface_name))
    virtual_network_resource_group = None
    if self.virtual_network_resource_group:
        virtual_network_resource_group = self.virtual_network_resource_group
    else:
        virtual_network_resource_group = self.resource_group
    if self.virtual_network_name:
        try:
            self.network_client.virtual_networks.list(virtual_network_resource_group, self.virtual_network_name)
            virtual_network_name = self.virtual_network_name
        except CloudError as exc:
            self.fail('Error: fetching virtual network {0} - {1}'.format(self.virtual_network_name, str(exc)))
    else:
        no_vnets_msg = 'Error: unable to find virtual network in resource group {0}. A virtual network with at least one subnet must exist in order to create a NIC for the virtual machine.'.format(self.resource_group)
        virtual_network_name = None
        try:
            vnets = self.network_client.virtual_networks.list(self.resource_group)
        except CloudError:
            self.log('cloud error!')
            self.fail(no_vnets_msg)
        for vnet in vnets:
            virtual_network_name = vnet.name
            self.log('vnet name: {0}'.format(vnet.name))
            break
        if (not virtual_network_name):
            self.fail(no_vnets_msg)
    if self.subnet_name:
        try:
            subnet = self.network_client.subnets.get(self.resource_group, virtual_network_name, self.subnet_name)
            subnet_id = subnet.id
        except Exception as exc:
            self.fail('Error: fetching subnet {0} - {1}'.format(self.subnet_name, str(exc)))
    else:
        no_subnets_msg = 'Error: unable to find a subnet in virtual network {0}. A virtual network with at least one subnet must exist in order to create a NIC for the virtual machine.'.format(virtual_network_name)
        subnet_id = None
        try:
            subnets = self.network_client.subnets.list(virtual_network_resource_group, virtual_network_name)
        except CloudError:
            self.fail(no_subnets_msg)
        for subnet in subnets:
            subnet_id = subnet.id
            self.log('subnet id: {0}'.format(subnet_id))
            break
        if (not subnet_id):
            self.fail(no_subnets_msg)
    self.results['actions'].append('Created default public IP {0}'.format((self.name + '01')))
    pip = self.create_default_pip(self.resource_group, self.location, (self.name + '01'), self.public_ip_allocation_method)
    self.results['actions'].append('Created default security group {0}'.format((self.name + '01')))
    group = self.create_default_securitygroup(self.resource_group, self.location, (self.name + '01'), self.os_type, self.open_ports)
    parameters = self.network_models.NetworkInterface(location=self.location, ip_configurations=[self.network_models.NetworkInterfaceIPConfiguration(private_ip_allocation_method='Dynamic')])
    parameters.ip_configurations[0].subnet = self.network_models.Subnet(id=subnet_id)
    parameters.ip_configurations[0].name = 'default'
    parameters.network_security_group = self.network_models.NetworkSecurityGroup(id=group.id, location=group.location, resource_guid=group.resource_guid)
    parameters.ip_configurations[0].public_ip_address = self.network_models.PublicIPAddress(id=pip.id, location=pip.location, resource_guid=pip.resource_guid)
    self.log('Creating NIC {0}'.format(network_interface_name))
    self.log(self.serialize_obj(parameters, 'NetworkInterface'), pretty_print=True)
    self.results['actions'].append('Created NIC {0}'.format(network_interface_name))
    try:
        poller = self.network_client.network_interfaces.create_or_update(self.resource_group, network_interface_name, parameters)
        new_nic = self.get_poller_result(poller)
    except Exception as exc:
        self.fail('Error creating network interface {0} - {1}'.format(network_interface_name, str(exc)))
    return new_nic