def remove_hosts_port_group(self, hosts):
    '\n        Function to remove port group from given host\n        Args:\n            hosts: List of host system\n        '
    for host in hosts:
        self.remove_host_port_group(host_system=host, portgroup_name=self.portgroup_name, vswitch_name=self.switch_name)