def get_existing(self):
    'get existing info'
    if self.intf_info:
        self.existing['interface'] = self.intf_info['ifName']
        self.existing['mode'] = self.intf_info['linkType']
        self.existing['switchport'] = self.intf_info['l2Enable']
        self.existing['access_vlan'] = self.intf_info['pvid']
        self.existing['native_vlan'] = self.intf_info['pvid']
        self.existing['trunk_vlans'] = self.intf_info['trunkVlans']