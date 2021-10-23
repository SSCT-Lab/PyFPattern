def config_rr(self):
    'Configure RR'
    if self.conf_exist:
        return
    if self.bgp_instance:
        view_cmd = ('bgp %s instance %s' % (self.as_number, self.bgp_instance))
    else:
        view_cmd = ('bgp %s' % self.as_number)
    self.cli_add_command(view_cmd)
    if (self.bgp_evpn_enable == 'disable'):
        self.cli_add_command('undo l2vpn-family evpn')
    else:
        self.cli_add_command('l2vpn-family evpn')
        if (self.reflect_client and (self.reflect_client != self.cur_config['reflect_client'])):
            if (self.reflect_client == 'enable'):
                self.cli_add_command(('peer %s enable' % self.peer))
                self.cli_add_command(('peer %s reflect-client' % self.peer))
            else:
                self.cli_add_command(('undo peer %s reflect-client' % self.peer))
                self.cli_add_command(('undo peer %s enable' % self.peer))
        if (self.cur_config['bgp_evpn_enable'] == 'enable'):
            if (self.policy_vpn_target and (self.policy_vpn_target != self.cur_config['policy_vpn_target'])):
                if (self.policy_vpn_target == 'enable'):
                    self.cli_add_command('policy vpn-target')
                else:
                    self.cli_add_command('undo policy vpn-target')
        elif (self.policy_vpn_target and (self.policy_vpn_target == 'disable')):
            self.cli_add_command('undo policy vpn-target')
    if self.commands:
        self.cli_load_config(self.commands)
        self.changed = True