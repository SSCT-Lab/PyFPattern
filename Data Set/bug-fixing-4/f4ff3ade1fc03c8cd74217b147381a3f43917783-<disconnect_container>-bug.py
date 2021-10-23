def disconnect_container(self, container_name):
    if (not self.check_mode):
        self.client.disconnect_container_from_network(container_name, self.parameters.network_name)
    self.results['actions'].append(('Disconnected container %s' % (container_name,)))
    self.results['changed'] = True
    self.diff_tracker.add('connected.{0}'.format(container_name), parameter=False, active=True)