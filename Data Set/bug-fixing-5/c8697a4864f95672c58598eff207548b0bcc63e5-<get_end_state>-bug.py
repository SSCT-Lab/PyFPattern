def get_end_state(self):
    'get end state info'
    if self.intf_info:
        end_info = self.get_interface_dict(self.interface)
        if end_info:
            self.end_state['interface'] = end_info['ifName']
            self.end_state['mode'] = end_info['linkType']
            self.end_state['switchport'] = end_info['l2Enable']
            self.end_state['access_vlan'] = end_info['pvid']
            self.end_state['native_vlan'] = end_info['pvid']
            self.end_state['trunk_vlans'] = end_info['trunkVlans']