

def modify_connection_vlan(self):
    cmd = [self.nmcli_bin]
    cmd.append('con')
    cmd.append('mod')
    cmd.append('con-name')
    params = {
        'vlan.parent': self.vlandev,
        'vlan.id': self.vlanid,
        'ipv4.address': self.ip4,
        'ipv4.geteway': self.gw4,
        'ipv4.dns': self.dns4,
        'ipv6.address': self.ip6,
        'ipv6.gateway': self.gw6,
        'ipv6.dns': self.dns6,
        'autoconnect': self.bool_to_string(self.autoconnect),
    }
    for (k, v) in params.items():
        cmd.extend([k, v])
    return cmd
