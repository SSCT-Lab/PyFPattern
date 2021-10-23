def _fill_host_variables(self, server_id, server_info):
    targeted_attributes = ('arch', 'commercial_type', 'organization', 'state', 'hostname', 'state')
    for attribute in targeted_attributes:
        self.inventory.set_variable(server_id, attribute, server_info[attribute])
    self.inventory.set_variable(server_id, 'tags', server_info['tags'])
    self.inventory.set_variable(server_id, 'ipv4', server_info['public_ip']['address'])