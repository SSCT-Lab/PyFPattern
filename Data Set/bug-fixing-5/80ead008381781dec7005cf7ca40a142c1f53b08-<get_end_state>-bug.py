def get_end_state(self):
    ' get_end_state'
    if self.intf_info:
        end_info = self.get_interface_dict(self.interface)
        if end_info:
            self.end_state['interface'] = end_info['ifName']
            self.end_state['mtu'] = end_info['ifMtu']
    if self.intf_info:
        if (not self.end_state['interface']):
            self.end_state['interface'] = self.interface
        if (self.state == 'absent'):
            self.end_state['jumboframe'] = ('jumboframe enable %s %s' % (9216, 1518))
        elif ((not self.jbf_max) and (not self.jbf_min)):
            if (len(self.jbf_config) != 2):
                return
            self.end_state['jumboframe'] = ('jumboframe enable %s %s' % (self.jbf_config[0], self.jbf_config[1]))
        elif self.jbf_min:
            self.end_state['jumboframe'] = ('jumboframe enable %s %s' % (self.jbf_max, self.jbf_min))
        else:
            self.end_state['jumboframe'] = ('jumboframe enable %s %s' % (self.jbf_max, 1518))