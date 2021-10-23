def __init__(self, module):
    self._module = module
    self._warnings = []
    self._gather_subset = module.params.get('gather_subset')
    self._gather_network_resources = module.params.get('gather_network_resources')
    self._connection = get_resource_connection(module)
    self.ansible_facts = {
        'ansible_network_resources': {
            
        },
    }
    self.ansible_facts['ansible_net_gather_network_resources'] = list()
    self.ansible_facts['ansible_net_gather_subset'] = list()
    if (not self._gather_subset):
        self._gather_subset = ['!config']
    if (not self._gather_network_resources):
        self._gather_network_resources = ['!all']