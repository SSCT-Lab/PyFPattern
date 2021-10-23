

def present(self):
    different = False
    differences = []
    if self.existing_network:
        (different, differences) = self.has_different_config(self.existing_network)
    if (self.parameters.force or different):
        self.remove_network()
        self.existing_network = None
    self.create_network()
    self.connect_containers()
    if (not self.parameters.appends):
        self.disconnect_missing()
    if (self.diff or self.check_mode or self.parameters.debug):
        self.results['diff'] = differences
    if ((not self.check_mode) and (not self.parameters.debug)):
        self.results.pop('actions')
    self.results['ansible_facts'] = {
        'docker_network': self.get_existing_network(),
    }
