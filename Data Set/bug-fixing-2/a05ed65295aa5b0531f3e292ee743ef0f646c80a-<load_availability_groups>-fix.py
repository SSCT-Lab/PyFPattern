

def load_availability_groups(self, node, datacenter):
    "check the health of each service on a node and add the node to either\n        an 'available' or 'unavailable' grouping. The suffix for each group can be\n        controlled from the config"
    if self.config.has_config('availability'):
        for (service_name, service) in iteritems(node['Services']):
            for node in self.consul_api.health.service(service_name)[1]:
                for check in node['Checks']:
                    if (check['ServiceName'] == service_name):
                        ok = ('passing' == check['Status'])
                        if ok:
                            suffix = self.config.get_availability_suffix('available_suffix', '_available')
                        else:
                            suffix = self.config.get_availability_suffix('unavailable_suffix', '_unavailable')
                        self.add_node_to_map(self.nodes_by_availability, (service_name + suffix), node['Node'])
