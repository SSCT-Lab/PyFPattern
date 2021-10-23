def get_update_cmd(self):
    'Get updated commands'
    if self.conf_exsit:
        return
    cli_str = ''
    if (self.state == 'present'):
        if self.address:
            if (self.peer_type == 'Server'):
                if (self.ip_ver == 'IPv4'):
                    cli_str = ('%s %s' % ('ntp unicast-server', self.address))
                else:
                    cli_str = ('%s %s' % ('ntp unicast-server ipv6', self.address))
            elif (self.peer_type == 'Peer'):
                if (self.ip_ver == 'IPv4'):
                    cli_str = ('%s %s' % ('ntp unicast-peer', self.address))
                else:
                    cli_str = ('%s %s' % ('ntp unicast-peer ipv6', self.address))
            if self.key_id:
                cli_str = ('%s %s %s' % (cli_str, 'authentication-keyid', self.key_id))
            if self.interface:
                cli_str = ('%s %s %s' % (cli_str, 'source-interface', self.interface))
            if (self.vpn_name and (self.vpn_name != '_public_')):
                cli_str = ('%s %s %s' % (cli_str, 'vpn-instance', self.vpn_name))
            if (self.is_preferred == 'enable'):
                cli_str = ('%s %s' % (cli_str, 'preferred'))
    elif self.address:
        if (self.peer_type == 'Server'):
            if (self.ip_ver == 'IPv4'):
                cli_str = ('%s %s' % ('undo ntp unicast-server', self.address))
            else:
                cli_str = ('%s %s' % ('undo ntp unicast-server ipv6', self.address))
        elif (self.peer_type == 'Peer'):
            if (self.ip_ver == 'IPv4'):
                cli_str = ('%s %s' % ('undo ntp unicast-peer', self.address))
            else:
                cli_str = ('%s %s' % ('undo ntp unicast-peer ipv6', self.address))
        if (self.vpn_name and (self.vpn_name != '_public_')):
            cli_str = ('%s %s %s' % (cli_str, 'vpn-instance', self.vpn_name))
    self.updates_cmd.append(cli_str)