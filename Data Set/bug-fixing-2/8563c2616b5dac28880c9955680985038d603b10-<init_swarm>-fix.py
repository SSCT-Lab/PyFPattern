

def init_swarm(self):
    if self.client.check_if_swarm_manager():
        self.__update_swarm()
        return
    if (not self.check_mode):
        try:
            self.client.init_swarm(advertise_addr=self.parameters.advertise_addr, listen_addr=self.parameters.listen_addr, force_new_cluster=self.parameters.force_new_cluster, swarm_spec=self.parameters.spec)
        except APIError as exc:
            self.client.fail(('Can not create a new Swarm Cluster: %s' % to_native(exc)))
    if (not self.client.check_if_swarm_manager()):
        if (not self.check_mode):
            self.client.fail('Swarm not created or other error!')
    self.inspect_swarm()
    self.results['actions'].append(('New Swarm cluster created: %s' % self.swarm_info.get('ID')))
    self.differences.add('state', parameter='present', active='absent')
    self.results['changed'] = True
    self.results['swarm_facts'] = {
        'JoinTokens': self.swarm_info.get('JoinTokens'),
    }
