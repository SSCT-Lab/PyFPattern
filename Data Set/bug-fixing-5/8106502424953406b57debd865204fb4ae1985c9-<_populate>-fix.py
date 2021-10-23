def _populate(self):
    raw_params = dict(docker_host=self.get_option('docker_host'), tls=self.get_option('tls'), tls_verify=self.get_option('tls_verify'), key_path=self.get_option('key_path'), cacert_path=self.get_option('cacert_path'), cert_path=self.get_option('cert_path'), tls_hostname=self.get_option('tls_hostname'), api_version=self.get_option('api_version'), timeout=self.get_option('timeout'), ssl_version=self.get_option('ssl_version'), debug=None)
    update_tls_hostname(raw_params)
    connect_params = get_connect_params(raw_params, fail_function=self._fail)
    self.client = docker.DockerClient(**connect_params)
    self.inventory.add_group('all')
    self.inventory.add_group('manager')
    self.inventory.add_group('worker')
    self.inventory.add_group('leader')
    self.inventory.add_group('nonleaders')
    if self.get_option('include_host_uri'):
        if self.get_option('include_host_uri_port'):
            host_uri_port = str(self.get_option('include_host_uri_port'))
        elif (self.get_option('tls') or self.get_option('tls_verify')):
            host_uri_port = '2376'
        else:
            host_uri_port = '2375'
    try:
        self.nodes = self.client.nodes.list()
        for self.node in self.nodes:
            self.node_attrs = self.client.nodes.get(self.node.id).attrs
            self.inventory.add_host(self.node_attrs['ID'])
            self.inventory.add_host(self.node_attrs['ID'], group=self.node_attrs['Spec']['Role'])
            self.inventory.set_variable(self.node_attrs['ID'], 'ansible_host', self.node_attrs['Status']['Addr'])
            if self.get_option('include_host_uri'):
                self.inventory.set_variable(self.node_attrs['ID'], 'ansible_host_uri', ((('tcp://' + self.node_attrs['Status']['Addr']) + ':') + host_uri_port))
            if self.get_option('verbose_output'):
                self.inventory.set_variable(self.node_attrs['ID'], 'docker_swarm_node_attributes', self.node_attrs)
            if ('ManagerStatus' in self.node_attrs):
                if self.node_attrs['ManagerStatus'].get('Leader'):
                    swarm_leader_ip = (parse_address(self.node_attrs['ManagerStatus']['Addr'])[0] or self.node_attrs['Status']['Addr'])
                    if self.get_option('include_host_uri'):
                        self.inventory.set_variable(self.node_attrs['ID'], 'ansible_host_uri', ((('tcp://' + swarm_leader_ip) + ':') + host_uri_port))
                    self.inventory.set_variable(self.node_attrs['ID'], 'ansible_host', swarm_leader_ip)
                    self.inventory.add_host(self.node_attrs['ID'], group='leader')
                else:
                    self.inventory.add_host(self.node_attrs['ID'], group='nonleaders')
            else:
                self.inventory.add_host(self.node_attrs['ID'], group='nonleaders')
            strict = self.get_option('strict')
            self._set_composite_vars(self.get_option('compose'), self.node_attrs, self.node_attrs['ID'], strict=strict)
            self._add_host_to_composed_groups(self.get_option('groups'), self.node_attrs, self.node_attrs['ID'], strict=strict)
            self._add_host_to_keyed_groups(self.get_option('keyed_groups'), self.node_attrs, self.node_attrs['ID'], strict=strict)
    except Exception as e:
        raise AnsibleError(('Unable to fetch hosts from Docker swarm API, this was the original exception: %s' % to_native(e)))