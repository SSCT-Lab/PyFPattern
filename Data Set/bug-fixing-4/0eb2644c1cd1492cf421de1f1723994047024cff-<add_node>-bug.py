def add_node(self, node):
    'Adds an node to the inventory and index.'
    if self.use_public_ip:
        dest = self.get_node_public_ip(node)
    else:
        dest = node.label
    self.index[dest] = node.api_id
    self.inventory[node.api_id] = [dest]
    self.push(self.inventory, self.get_datacenter_city(node), dest)
    self.push(self.inventory, node.display_group, dest)
    self.push(self.inventory, 'linode', dest)
    self.inventory['_meta']['hostvars'][dest] = self.get_host_info(node)