def add_hosts_port_group(self):
    '\n        Function to add port group to given hosts\n        '
    results = dict(changed=False, result=dict())
    host_change_list = []
    for host in self.host_obj_list:
        change = False
        results['result'][host.name] = dict(portgroup_name=self.portgroup_name, vlan_id=self.vlan_id, switch_name=self.switch_name)
        change = self.create_host_port_group(host, self.portgroup_name, self.vlan_id, self.switch_name, self.network_policy)
        host_change_list.append(change)
    if any(host_change_list):
        results['changed'] = True
    self.module.exit_json(**results)