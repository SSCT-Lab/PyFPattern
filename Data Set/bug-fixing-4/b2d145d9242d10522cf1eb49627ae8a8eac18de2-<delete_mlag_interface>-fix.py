def delete_mlag_interface(self):
    'delete mlag interface attribute info'
    if self.is_mlag_interface_info_exist():
        mlag_port = 'Eth-Trunk'
        mlag_port += self.eth_trunk_id
        conf_str = (CE_NC_SET_LACP_MLAG_INFO_HEAD % mlag_port)
        cmd = ('interface %s' % mlag_port)
        self.cli_add_command(cmd)
        if self.mlag_priority_id:
            cmd = ('lacp m-lag priority %s' % self.mlag_priority_id)
            conf_str += '<lacpMlagPriority></lacpMlagPriority>'
            self.cli_add_command(cmd, True)
        if self.mlag_system_id:
            cmd = ('lacp m-lag system-id %s' % self.mlag_system_id)
            conf_str += '<lacpMlagSysId></lacpMlagSysId>'
            self.cli_add_command(cmd, True)
        if self.commands:
            conf_str += CE_NC_SET_LACP_MLAG_INFO_TAIL
            recv_xml = set_nc_config(self.module, conf_str)
            if ('<ok/>' not in recv_xml):
                self.module.fail_json(msg='Error: set mlag interface atrribute info failed.')
            self.changed = True