def delete_snmp_target_host(self):
    ' Delete snmp target host operation '
    conf_str = (CE_DELETE_SNMP_TARGET_HOST_HEADER % self.host_name)
    if self.domain:
        conf_str += ('<domain>%s</domain>' % self.domain)
    if self.address:
        conf_str += ('<address>%s</address>' % self.address)
    if self.notify_type:
        conf_str += ('<notifyType>%s</notifyType>' % self.notify_type)
    if self.vpn_name:
        conf_str += ('<vpnInstanceName>%s</vpnInstanceName>' % self.vpn_name)
    if self.recv_port:
        conf_str += ('<portNumber>%s</portNumber>' % self.recv_port)
    if self.security_model:
        conf_str += ('<securityModel>%s</securityModel>' % self.security_model)
    if self.security_name:
        conf_str += ('<securityName>%s</securityName>' % self.security_name)
    if self.security_name_v3:
        conf_str += ('<securityNameV3>%s</securityNameV3>' % self.security_name_v3)
    if self.security_level:
        conf_str += ('<securityLevel>%s</securityLevel>' % self.security_level)
    if (self.is_public_net != 'no_use'):
        conf_str += ('<isPublicNet>%s</isPublicNet>' % self.is_public_net)
    if self.interface_name:
        conf_str += ('<interface-name>%s</interface-name>' % self.interface_name)
    conf_str += CE_DELETE_SNMP_TARGET_HOST_TAIL
    recv_xml = self.netconf_set_config(conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        self.module.fail_json(msg='Error: Delete snmp target host failed.')
    if (not self.address):
        cmd = ('undo snmp-agent target-host host-name %s ' % self.host_name)
    else:
        cmd = ('undo snmp-agent target-host trap address udp-domain %s ' % self.address)
        if self.recv_port:
            cmd += ('udp-port %s ' % self.recv_port)
        if self.interface_name:
            cmd += ('source %s ' % self.interface_name)
        if self.vpn_name:
            cmd += ('vpn-instance %s ' % self.vpn_name)
        if (self.is_public_net == 'true'):
            cmd += 'public-net '
        if ((self.security_model in ['v1', 'v2c']) and self.security_name):
            cmd += ('params securityname %s' % '******')
        if ((self.security_model == 'v3') and self.security_name_v3):
            cmd += ('params securityname %s' % self.security_name_v3)
    self.changed = True
    self.updates_cmd.append(cmd)