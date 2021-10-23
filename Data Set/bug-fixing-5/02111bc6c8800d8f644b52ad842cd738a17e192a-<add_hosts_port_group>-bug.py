def add_hosts_port_group(self, hosts):
    '\n        Function to add port group to given hosts\n        Args:\n            hosts: List of Host System\n        '
    for host in hosts:
        self.create_host_port_group(host, self.portgroup_name, self.vlan_id, self.switch_name, self.network_policy)