def remove_network(self):
    if self.existing_network:
        self.disconnect_all_containers()
        if (not self.check_mode):
            self.client.remove_network(self.parameters.network_name)
        self.results['actions'].append(('Removed network %s' % (self.parameters.network_name,)))
        self.results['changed'] = True