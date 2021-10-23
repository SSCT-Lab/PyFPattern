

def set_update_cmd(self):
    'set update command'
    if (not self.changed):
        return
    if (self.aftype == 'v4'):
        aftype = 'ip'
        maskstr = self.convert_len_to_mask(self.mask)
    else:
        aftype = 'ipv6'
        maskstr = self.mask
    if (self.next_hop is None):
        next_hop = ''
    else:
        next_hop = self.next_hop
    if (self.vrf == '_public_'):
        vrf = ''
    else:
        vrf = self.vrf
    if (self.destvrf == '_public_'):
        destvrf = ''
    else:
        destvrf = self.destvrf
    if (self.nhp_interface == 'Invalid0'):
        nhp_interface = ''
    else:
        nhp_interface = self.nhp_interface
    if (self.state == 'present'):
        if (self.vrf != '_public_'):
            if (self.destvrf != '_public_'):
                self.updates_cmd.append(('%s route-static vpn-instance %s %s %s vpn-instance %s %s' % (aftype, vrf, self.prefix, maskstr, destvrf, next_hop)))
            else:
                self.updates_cmd.append(('%s route-static vpn-instance %s %s %s %s %s' % (aftype, vrf, self.prefix, maskstr, nhp_interface, next_hop)))
        elif (self.destvrf != '_public_'):
            self.updates_cmd.append(('%s route-static %s %s vpn-instance %s %s' % (aftype, self.prefix, maskstr, self.destvrf, next_hop)))
        else:
            self.updates_cmd.append(('%s route-static %s %s %s %s' % (aftype, self.prefix, maskstr, nhp_interface, next_hop)))
        if self.pref:
            self.updates_cmd[0] += (' preference %s' % self.pref)
        if self.tag:
            self.updates_cmd[0] += (' tag %s' % self.tag)
        if self.description:
            self.updates_cmd[0] += (' description %s' % self.description)
    if (self.state == 'absent'):
        if (self.vrf != '_public_'):
            if (self.destvrf != '_public_'):
                self.updates_cmd.append(('undo %s route-static vpn-instance %s %s %s vpn-instance %s %s' % (aftype, vrf, self.prefix, maskstr, destvrf, next_hop)))
            else:
                self.updates_cmd.append(('undo %s route-static vpn-instance %s %s %s %s %s' % (aftype, vrf, self.prefix, maskstr, nhp_interface, next_hop)))
        elif (self.destvrf != '_public_'):
            self.updates_cmd.append(('undo %s route-static %s %s vpn-instance %s %s' % (aftype, self.prefix, maskstr, self.destvrf, self.next_hop)))
        else:
            self.updates_cmd.append(('undo %s route-static %s %s %s %s' % (aftype, self.prefix, maskstr, nhp_interface, next_hop)))
