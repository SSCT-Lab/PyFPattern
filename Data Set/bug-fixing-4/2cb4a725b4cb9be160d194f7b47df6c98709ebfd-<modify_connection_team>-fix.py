def modify_connection_team(self):
    cmd = [self.nmcli_bin, 'con', 'mod', self.conn_name]
    if (self.ip4 is not None):
        cmd.append('ipv4.address')
        cmd.append(self.ip4)
    if (self.gw4 is not None):
        cmd.append('ipv4.gateway')
        cmd.append(self.gw4)
    if (self.dns4 is not None):
        cmd.append('ipv4.dns')
        cmd.append(self.dns4)
    if (self.ip6 is not None):
        cmd.append('ipv6.address')
        cmd.append(self.ip6)
    if (self.gw6 is not None):
        cmd.append('ipv6.gateway')
        cmd.append(self.gw6)
    if (self.dns6 is not None):
        cmd.append('ipv6.dns')
        cmd.append(self.dns6)
    if (self.autoconnect is not None):
        cmd.append('autoconnect')
        cmd.append(self.bool_to_string(self.autoconnect))
    return cmd