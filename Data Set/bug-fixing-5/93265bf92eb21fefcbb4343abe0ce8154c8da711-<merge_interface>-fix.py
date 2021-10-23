def merge_interface(self, ifname, mtu):
    ' Merge interface mtu.'
    xmlstr = ''
    change = False
    command = ('interface %s' % ifname)
    self.cli_add_command(command)
    if (self.state == 'present'):
        if (mtu and (self.intf_info['ifMtu'] != mtu)):
            command = ('mtu %s' % mtu)
            self.cli_add_command(command)
            self.updates_cmd.append(('mtu %s' % mtu))
            change = True
    elif ((self.intf_info['ifMtu'] != '1500') and self.intf_info['ifMtu']):
        command = 'mtu 1500'
        self.cli_add_command(command)
        self.updates_cmd.append('undo mtu')
        change = True
    return