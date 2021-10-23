def delete_mlag_global(self):
    'delete mlag global attribute info'
    xml_str = ''
    if self.is_mlag_global_info_exist():
        if self.mlag_priority_id:
            cmd = ('lacp m-lag priority %s' % self.mlag_priority_id)
            xml_str += '<lacpMlagPriority></lacpMlagPriority>'
            self.cli_add_command(cmd, True)
        if self.mlag_system_id:
            cmd = ('lacp m-lag system-id %s' % self.mlag_system_id)
            xml_str += '<lacpMlagSysId></lacpMlagSysId>'
            self.cli_add_command(cmd, True)
        if (xml_str != ''):
            conf_str = ((CE_NC_SET_GLOBAL_LACP_MLAG_INFO_HEAD + xml_str) + CE_NC_SET_GLOBAL_LACP_MLAG_INFO_TAIL)
            recv_xml = set_nc_config(self.module, conf_str)
            if ('<ok/>' not in recv_xml):
                self.module.fail_json(msg='Error: set mlag interface atrribute info failed.')
            self.changed = True