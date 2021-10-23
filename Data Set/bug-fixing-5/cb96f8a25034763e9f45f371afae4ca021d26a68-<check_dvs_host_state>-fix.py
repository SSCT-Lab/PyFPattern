def check_dvs_host_state(self):
    self.dv_switch = find_dvs_by_name(self.content, self.switch_name)
    if (self.dv_switch is None):
        self.module.fail_json(msg=('A distributed virtual switch %s does not exist' % self.switch_name))
    self.uplink_portgroup = self.find_dvs_uplink_pg()
    if (self.uplink_portgroup is None):
        self.module.fail_json(msg=('An uplink portgroup does not exist on the distributed virtual switch %s' % self.switch_name))
    self.host = self.find_host_attached_dvs()
    if (self.host is None):
        self.host = find_hostsystem_by_name(self.content, self.esxi_hostname)
        if (self.host is None):
            self.module.fail_json(msg=('The esxi_hostname %s does not exist in vCenter' % self.esxi_hostname))
        return 'absent'
    elif self.check_uplinks():
        return 'present'
    else:
        return 'update'