def get_end_state(self):
    'get end state info'
    end_info = self.get_interface_dict(self.interface)
    if end_info:
        self.end_state['interface'] = end_info['ifName']
        self.end_state['switchport'] = end_info['l2Enable']
        self.end_state['mode'] = end_info['linkType']
        if (end_info['linkType'] == 'access'):
            self.end_state['access_pvid'] = end_info['pvid']
        elif (end_info['linkType'] == 'trunk'):
            self.end_state['trunk_pvid'] = end_info['pvid']
            self.end_state['trunk_vlans'] = end_info['trunkVlans']
        elif (end_info['linkType'] == 'hybrid'):
            self.end_state['hybrid_pvid'] = end_info['pvid']
            self.end_state['hybrid_untagged_vlans'] = end_info['untagVlans']
            self.end_state['hybrid_tagged_vlans'] = end_info['trunkVlans']
        else:
            self.end_state['dot1qtunnel_pvid'] = end_info['pvid']
    if (self.end_state == self.existing):
        self.changed = False