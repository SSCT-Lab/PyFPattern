

def create_network(self):
    if (not self.existing_network):
        params = dict(driver=self.parameters.driver, options=self.parameters.driver_options)
        ipam_pools = []
        if self.parameters.ipam_config:
            for ipam_pool in self.parameters.ipam_config:
                if (HAS_DOCKER_PY_2 or HAS_DOCKER_PY_3):
                    ipam_pools.append(IPAMPool(**ipam_pool))
                else:
                    ipam_pools.append(utils.create_ipam_pool(**ipam_pool))
        if (self.parameters.ipam_driver or ipam_pools):
            if (HAS_DOCKER_PY_2 or HAS_DOCKER_PY_3):
                params['ipam'] = IPAMConfig(driver=self.parameters.ipam_driver, pool_configs=ipam_pools)
            else:
                params['ipam'] = utils.create_ipam_config(driver=self.parameters.ipam_driver, pool_configs=ipam_pools)
        if (self.parameters.enable_ipv6 is not None):
            params['enable_ipv6'] = self.parameters.enable_ipv6
        if (self.parameters.internal is not None):
            params['internal'] = self.parameters.internal
        if (not self.check_mode):
            resp = self.client.create_network(self.parameters.network_name, **params)
            self.existing_network = self.client.inspect_network(resp['Id'])
        self.results['actions'].append(('Created network %s with driver %s' % (self.parameters.network_name, self.parameters.driver)))
        self.results['changed'] = True
