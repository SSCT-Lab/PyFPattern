

def create_default_securitygroup(self, resource_group, location, name, os_type, open_ports):
    "\n        Create a default security group <name>01 to associate with a network interface. If a security group matching\n        <name>01 exists, return it. Otherwise, create one.\n\n        :param resource_group: Resource group name\n        :param location: azure location name\n        :param name: base name to use for the security group\n        :param os_type: one of 'Windows' or 'Linux'. Determins any default rules added to the security group.\n        :param ssh_port: for os_type 'Linux' port used in rule allowing SSH access.\n        :param rdp_port: for os_type 'Windows' port used in rule allowing RDP access.\n        :return: security_group object\n        "
    security_group_name = (name + '01')
    group = None
    self.log('Create security group {0}'.format(security_group_name))
    self.log('Check to see if security group {0} exists'.format(security_group_name))
    try:
        group = self.network_client.network_security_groups.get(resource_group, security_group_name)
    except CloudError:
        pass
    if group:
        self.log('Security group {0} found.'.format(security_group_name))
        self.check_provisioning_state(group)
        return group
    parameters = NetworkSecurityGroup()
    parameters.location = location
    if (not open_ports):
        if (os_type == 'Linux'):
            parameters.security_rules = [SecurityRule('Tcp', '*', '*', 'Allow', 'Inbound', description='Allow SSH Access', source_port_range='*', destination_port_range='22', priority=100, name='SSH')]
            parameters.location = location
        else:
            parameters.security_rules = [SecurityRule('Tcp', '*', '*', 'Allow', 'Inbound', description='Allow RDP port 3389', source_port_range='*', destination_port_range='3389', priority=100, name='RDP01'), SecurityRule('Tcp', '*', '*', 'Allow', 'Inbound', description='Allow RDP port 5986', source_port_range='*', destination_port_range='5986', priority=101, name='RDP01')]
    else:
        parameters.security_rules = []
        priority = 100
        for port in open_ports:
            priority += 1
            rule_name = 'Rule_{0}'.format(priority)
            parameters.security_rules.append(SecurityRule('Tcp', '*', '*', 'Allow', 'Inbound', source_port_range='*', destination_port_range=str(port), priority=priority, name=rule_name))
    self.log('Creating default security group {0}'.format(security_group_name))
    try:
        poller = self.network_client.network_security_groups.create_or_update(resource_group, security_group_name, parameters)
    except Exception as exc:
        self.fail('Error creating default security rule {0} - {1}'.format(security_group_name, str(exc)))
    return self.get_poller_result(poller)
