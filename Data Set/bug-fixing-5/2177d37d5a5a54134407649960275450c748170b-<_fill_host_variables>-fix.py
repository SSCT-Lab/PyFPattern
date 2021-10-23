def _fill_host_variables(self, host, server_info):
    targeted_attributes = ('arch', 'commercial_type', 'id', 'organization', 'state', 'hostname', 'state')
    for attribute in targeted_attributes:
        self.inventory.set_variable(host, attribute, server_info[attribute])
    self.inventory.set_variable(host, 'tags', server_info['tags'])
    if extract_public_ipv6(server_info=server_info):
        self.inventory.set_variable(host, 'public_ipv6', extract_public_ipv6(server_info=server_info))
    if extract_public_ipv4(server_info=server_info):
        self.inventory.set_variable(host, 'public_ipv4', extract_public_ipv4(server_info=server_info))
        self.inventory.set_variable(host, 'ansible_host', extract_public_ipv4(server_info=server_info))