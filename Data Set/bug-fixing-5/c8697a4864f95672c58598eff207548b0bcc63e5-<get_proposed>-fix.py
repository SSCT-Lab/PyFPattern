def get_proposed(self):
    'get proposed info'
    self.proposed['state'] = self.state
    self.proposed['interface'] = self.interface
    self.proposed['mode'] = self.mode
    if self.mode:
        if (self.mode == 'access'):
            self.proposed['access_pvid'] = self.default_vlan
        elif (self.mode == 'trunk'):
            self.proposed['pvid_vlan'] = self.pvid_vlan
            self.proposed['trunk_vlans'] = self.trunk_vlans
        elif (self.mode == 'hybrid'):
            self.proposed['pvid_vlan'] = self.pvid_vlan
            self.proposed['untagged_vlans'] = self.untagged_vlans
            self.proposed['tagged_vlans'] = self.tagged_vlans
        else:
            self.proposed['dot1qtunnel_pvid'] = self.default_vlan