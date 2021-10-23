def config_nets_export_ip_ver(self):
    'Configures the version number of the exported packets carrying IPv4 flow statistics'
    cmd = ('netstream export ip version %s' % self.version)
    if (self.version == '5'):
        if (self.as_option == 'origin'):
            cmd += ' origin-as'
        elif (self.as_option == 'peer'):
            cmd += ' peer-as'
    else:
        if (self.as_option == 'origin'):
            cmd += ' origin-as'
        elif (self.as_option == 'peer'):
            cmd += ' peer-as'
        if (self.bgp_netxhop == 'enable'):
            cmd += ' bgp-nexthop'
    if (cmd == 'netstream export ip version 5'):
        cmd_tmp = 'netstream export ip version'
        if is_config_exist(self.config, cmd_tmp):
            if (self.state == 'present'):
                self.cli_add_command(cmd, False)
        else:
            self.exist_conf['version'] = self.version
        return
    if is_config_exist(self.config, cmd):
        self.exist_conf['version'] = self.version
        self.exist_conf['as_option'] = self.as_option
        self.exist_conf['bgp_netxhop'] = self.bgp_netxhop
        if (self.state == 'present'):
            return
        else:
            undo = True
    elif (self.state == 'absent'):
        return
    else:
        undo = False
    self.cli_add_command(cmd, undo)