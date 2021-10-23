def get_existing(self):
    'get existing info'
    if self.intf_info:
        self.existing['interface'] = self.intf_info['ifName']
        self.existing['switchport'] = self.intf_info['l2Enable']
        self.existing['mode'] = self.intf_info['linkType']
        if (self.intf_info['linkType'] == 'access'):
            self.existing['access_pvid'] = self.intf_info['pvid']
        elif (self.intf_info['linkType'] == 'trunk'):
            self.existing['trunk_pvid'] = self.intf_info['pvid']
            self.existing['trunk_vlans'] = self.intf_info['trunkVlans']
        elif (self.intf_info['linkType'] == 'hybrid'):
            self.existing['hybrid_pvid'] = self.intf_info['pvid']
            self.existing['hybrid_untagged_vlans'] = self.intf_info['untagVlans']
            self.existing['hybrid_tagged_vlans'] = self.intf_info['trunkVlans']
        else:
            self.existing['dot1qtunnel_pvid'] = self.intf_info['pvid']