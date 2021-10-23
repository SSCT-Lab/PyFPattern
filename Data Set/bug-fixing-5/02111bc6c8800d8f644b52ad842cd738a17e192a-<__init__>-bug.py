def __init__(self, module):
    super(PyVmomiHelper, self).__init__(module)
    self.hosts = self.params['hosts']
    self.cluster = self.params['cluster_name']
    self.portgroup_name = self.params['portgroup_name']
    self.switch_name = self.params['switch_name']
    self.vlan_id = self.params['vlan_id']
    self.promiscuous_mode = self.params['network_policy'].get('promiscuous_mode')
    self.forged_transmits = self.params['network_policy'].get('forged_transmits')
    self.mac_changes = self.params['network_policy'].get('mac_changes')
    self.network_policy = self.create_network_policy()
    self.changed = False
    self.state = self.params['state']