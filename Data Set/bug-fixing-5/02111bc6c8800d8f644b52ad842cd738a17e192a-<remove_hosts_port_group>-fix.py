def remove_hosts_port_group(self):
    '\n        Function to remove port group from given host\n        '
    results = dict(changed=False, result=dict())
    host_change_list = []
    for host in self.host_obj_list:
        change = False
        results['result'][host.name] = dict(portgroup_name=self.portgroup_name, vlan_id=self.vlan_id, switch_name=self.switch_name)
        change = self.remove_host_port_group(host_system=host, portgroup_name=self.portgroup_name, vswitch_name=self.switch_name)
        host_change_list.append(change)
    if any(host_change_list):
        results['changed'] = True
    self.module.exit_json(**results)