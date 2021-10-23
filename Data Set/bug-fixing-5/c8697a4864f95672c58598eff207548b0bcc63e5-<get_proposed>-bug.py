def get_proposed(self):
    'get proposed info'
    self.proposed['state'] = self.state
    self.proposed['interface'] = self.interface
    self.proposed['mode'] = self.mode
    self.proposed['access_vlan'] = self.access_vlan
    self.proposed['native_vlan'] = self.native_vlan
    self.proposed['trunk_vlans'] = self.trunk_vlans