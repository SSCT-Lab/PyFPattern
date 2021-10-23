def _populate(self):
    self.client = docker.DockerClient(base_url=self.get_option('host'), tls=self._get_tls_connect_params())
    self.inventory.add_group('all')
    self.inventory.add_group('manager')
    self.inventory.add_group('worker')
    self.inventory.add_group('leader')
    try:
        self.nodes = self.client.nodes.list()
        for self.node in self.nodes:
            self.node_attrs = self.client.nodes.get(self.node.id).attrs
            self.inventory.add_host(self.node_attrs['ID'])
            self.inventory.add_host(self.node_attrs['ID'], group=self.node_attrs['Spec']['Role'])
            self.inventory.set_variable(self.node_attrs['ID'], 'ansible_host', self.node_attrs['Status']['Addr'])
            if self.get_option('verbose_output', True):
                self.inventory.set_variable(self.node_attrs['ID'], 'docker_swarm_node_attributes', self.node_attrs)
            if ('ManagerStatus' in self.node_attrs):
                if self.node_attrs['ManagerStatus'].get('Leader'):
                    self.inventory.add_host(self.node_attrs['ID'], group='leader')
            strict = self.get_option('strict')
            self._set_composite_vars(self.get_option('compose'), self.node_attrs, self.node_attrs['ID'], strict=strict)
            self._add_host_to_composed_groups(self.get_option('groups'), self.node_attrs, self.node_attrs['ID'], strict=strict)
            self._add_host_to_keyed_groups(self.get_option('keyed_groups'), self.node_attrs, self.node_attrs['ID'], strict=strict)
    except Exception as e:
        raise AnsibleError(('Unable to fetch hosts from Docker swarm API, this was the original exception: %s' % to_native(e)))