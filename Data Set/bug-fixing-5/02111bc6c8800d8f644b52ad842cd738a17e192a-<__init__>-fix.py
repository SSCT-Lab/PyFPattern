def __init__(self, module):
    super(PyVmomiHelper, self).__init__(module)
    hosts = self.params['hosts']
    cluster = self.params['cluster_name']
    self.portgroup_name = self.params['portgroup_name']
    self.switch_name = self.params['switch_name']
    self.vlan_id = self.params['vlan_id']
    self.promiscuous_mode = self.params['network_policy'].get('promiscuous_mode')
    self.forged_transmits = self.params['network_policy'].get('forged_transmits')
    self.mac_changes = self.params['network_policy'].get('mac_changes')
    self.network_policy = self.create_network_policy()
    self.state = self.params['state']
    self.host_obj_list = []
    if (cluster and self.find_cluster_by_name(cluster_name=cluster)):
        self.host_obj_list = self.get_all_hosts_by_cluster(cluster_name=cluster)
    elif hosts:
        for host in hosts:
            host_system = self.find_hostsystem_by_name(host_name=host)
            if host_system:
                self.host_obj_list.append(host_system)
            else:
                self.module.fail_json(msg=('Failed to find ESXi %s' % host))