def create_network(self):
    if (not self.existing_network):
        params = dict(driver=self.parameters.driver, options=self.parameters.driver_options)
        ipam_pools = []
        if self.parameters.ipam_config:
            for ipam_pool in self.parameters.ipam_config:
                if (LooseVersion(docker_version) >= LooseVersion('2.0.0')):
                    ipam_pools.append(IPAMPool(**ipam_pool))
                else:
                    ipam_pools.append(utils.create_ipam_pool(**ipam_pool))
        if (self.parameters.ipam_driver or self.parameters.ipam_driver_options or ipam_pools):
            if (LooseVersion(docker_version) >= LooseVersion('2.0.0')):
                params['ipam'] = IPAMConfig(driver=self.parameters.ipam_driver, pool_configs=ipam_pools, options=self.parameters.ipam_driver_options)
            else:
                params['ipam'] = utils.create_ipam_config(driver=self.parameters.ipam_driver, pool_configs=ipam_pools)
        if (self.parameters.enable_ipv6 is not None):
            params['enable_ipv6'] = self.parameters.enable_ipv6
        if (self.parameters.internal is not None):
            params['internal'] = self.parameters.internal
        if (self.parameters.scope is not None):
            params['scope'] = self.parameters.scope
        if (self.parameters.attachable is not None):
            params['attachable'] = self.parameters.attachable
        if self.parameters.labels:
            params['labels'] = self.parameters.labels
        if (not self.check_mode):
            resp = self.client.create_network(self.parameters.name, **params)
            self.client.report_warnings(resp, ['Warning'])
            self.existing_network = self.client.get_network(id=resp['Id'])
        self.results['actions'].append(('Created network %s with driver %s' % (self.parameters.name, self.parameters.driver)))
        self.results['changed'] = True