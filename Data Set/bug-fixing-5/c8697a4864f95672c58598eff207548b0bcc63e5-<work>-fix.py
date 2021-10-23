def work(self):
    'worker'
    self.check_params()
    if (not self.intf_info):
        self.module.fail_json(msg='Error: interface does not exist.')
    self.get_existing()
    self.get_proposed()
    if ((self.state == 'present') or (self.state == 'absent')):
        if (self.mode == 'access'):
            self.merge_access_vlan(self.interface, self.default_vlan)
        elif (self.mode == 'trunk'):
            self.merge_trunk_vlan(self.interface, self.pvid_vlan, self.trunk_vlans)
        elif (self.mode == 'hybrid'):
            self.merge_hybrid_vlan(self.interface, self.pvid_vlan, self.tagged_vlans, self.untagged_vlans)
        else:
            self.merge_dot1qtunnel_vlan(self.interface, self.default_vlan)
    else:
        self.default_switchport(self.interface)
    self.get_end_state()
    self.results['changed'] = self.changed
    self.results['proposed'] = self.proposed
    self.results['existing'] = self.existing
    self.results['end_state'] = self.end_state
    if self.changed:
        self.results['updates'] = self.updates_cmd
    else:
        self.results['updates'] = list()
    self.module.exit_json(**self.results)