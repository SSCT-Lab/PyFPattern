

def _set_server_attributes(self, server):
    self.inventory.set_variable(server.name, 'id', to_native(server.id))
    self.inventory.set_variable(server.name, 'name', to_native(server.name))
    self.inventory.set_variable(server.name, 'status', to_native(server.status))
    self.inventory.set_variable(server.name, 'type', to_native(server.server_type.name))
    self.inventory.set_variable(server.name, 'ipv4', to_native(server.public_net.ipv4.ip))
    self.inventory.set_variable(server.name, 'ipv6_network', to_native(server.public_net.ipv6.network))
    self.inventory.set_variable(server.name, 'ipv6_network_mask', to_native(server.public_net.ipv6.network_mask))
    if (self.get_option('connect_with') == 'public_ipv4'):
        self.inventory.set_variable(server.name, 'ansible_host', to_native(server.public_net.ipv4.ip))
    elif (self.get_option('connect_with') == 'hostname'):
        self.inventory.set_variable(server.name, 'ansible_host', to_native(server.name))
    elif (self.get_option('connect_with') == 'ipv4_dns_ptr'):
        self.inventory.set_variable(server.name, 'ansible_host', to_native(server.public_net.ipv4.dns_ptr))
    self.inventory.set_variable(server.name, 'server_type', to_native(server.image.name))
    self.inventory.set_variable(server.name, 'datacenter', to_native(server.datacenter.name))
    self.inventory.set_variable(server.name, 'location', to_native(server.datacenter.location.name))
    self.inventory.set_variable(server.name, 'image_id', to_native(server.image.id))
    self.inventory.set_variable(server.name, 'image_name', to_native(server.image.name))
    self.inventory.set_variable(server.name, 'image_os_flavor', to_native(server.image.os_flavor))
