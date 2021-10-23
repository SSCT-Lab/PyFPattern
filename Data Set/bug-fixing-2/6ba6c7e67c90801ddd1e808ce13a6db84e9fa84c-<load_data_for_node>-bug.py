

def load_data_for_node(self, node, datacenter):
    'loads the data for a sinle node adding it to various groups based on\n        metadata retrieved from the kv store and service availability'
    if (self.config.suffixes == 'true'):
        (index, node_data) = self.consul_api.catalog.node(node, dc=datacenter)
    else:
        node_data = self.consul_get_node_inmemory(node)
    node = node_data['Node']
    self.add_node_to_map(self.nodes, 'all', node)
    self.add_metadata(node_data, 'consul_datacenter', datacenter)
    self.add_metadata(node_data, 'consul_nodename', node['Node'])
    self.load_groups_from_kv(node_data)
    self.load_node_metadata_from_kv(node_data)
    if (self.config.suffixes == 'true'):
        self.load_availability_groups(node_data, datacenter)
        for (name, service) in node_data['Services'].items():
            self.load_data_from_service(name, service, node_data)
