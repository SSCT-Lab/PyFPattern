def connect_containers(self):
    for name in self.parameters.connected:
        if (not self.is_container_connected(name)):
            if (not self.check_mode):
                self.client.connect_container_to_network(name, self.parameters.name)
            self.results['actions'].append(('Connected container %s' % (name,)))
            self.results['changed'] = True
            self.diff_tracker.add('connected.{0}'.format(name), parameter=True, active=False)