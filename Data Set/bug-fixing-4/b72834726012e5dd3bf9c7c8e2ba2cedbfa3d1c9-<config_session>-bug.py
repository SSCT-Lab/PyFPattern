def config_session(self):
    'configures bfd session'
    xml_str = ''
    cmd_list = list()
    if (not self.session_name):
        return xml_str
    if (self.bfd_dict['global'].get('bfdEnable', 'false') != 'true'):
        self.module.fail_json(msg='Error: Please enable BFD globally first.')
    xml_str = ('<sessName>%s</sessName>' % self.session_name)
    cmd_session = ('bfd %s' % self.session_name)
    if (self.state == 'present'):
        if (not self.bfd_dict['session']):
            if ((not self.dest_addr) and (not self.use_default_ip)):
                self.module.fail_json(msg='Error: dest_addr or use_default_ip must be set when bfd session is creating.')
            if self.create_type:
                xml_str += ('<createType>SESS_%s</createType>' % self.create_type.upper())
            else:
                xml_str += '<createType>SESS_STATIC</createType>'
            xml_str += '<linkType>IP</linkType>'
            cmd_session += ' bind'
            if self.addr_type:
                xml_str += ('<addrType>%s</addrType>' % self.addr_type.upper())
            else:
                xml_str += '<addrType>IPV4</addrType>'
            if self.dest_addr:
                xml_str += ('<destAddr>%s</destAddr>' % self.dest_addr)
                cmd_session += (' peer-%s %s' % (('ipv6' if (self.addr_type == 'ipv6') else 'ip'), self.dest_addr))
            if self.use_default_ip:
                xml_str += ('<useDefaultIp>%s</useDefaultIp>' % str(self.use_default_ip).lower())
                cmd_session += ' peer-ip default-ip'
            if self.vrf_name:
                xml_str += ('<vrfName>%s</vrfName>' % self.vrf_name)
                cmd_session += (' vpn-instance %s' % self.vrf_name)
            if self.out_if_name:
                xml_str += ('<outIfName>%s</outIfName>' % self.out_if_name)
                cmd_session += (' interface %s' % self.out_if_name.lower())
            if self.src_addr:
                xml_str += ('<srcAddr>%s</srcAddr>' % self.src_addr)
                cmd_session += (' source-%s %s' % (('ipv6' if (self.addr_type == 'ipv6') else 'ip'), self.src_addr))
            if (self.create_type == 'auto'):
                cmd_session += ' auto'
        elif (not self.is_session_match()):
            self.module.fail_json(msg='Error: The specified BFD configuration view has been created.')
        else:
            pass
    else:
        if (not self.bfd_dict['session']):
            self.module.fail_json(msg='Error: BFD session is not exist.')
        if (not self.is_session_match()):
            self.module.fail_json(msg='Error: BFD session parameter is invalid.')
    if (self.state == 'present'):
        if xml_str.endswith('</sessName>'):
            return ''
        else:
            cmd_list.insert(0, cmd_session)
            self.updates_cmd.extend(cmd_list)
            return (('<bfdCfgSessions><bfdCfgSession operation="merge">' + xml_str) + '</bfdCfgSession></bfdCfgSessions>')
    else:
        cmd_list.append(('undo ' + cmd_session))
        self.updates_cmd.extend(cmd_list)
        return (('<bfdCfgSessions><bfdCfgSession operation="delete">' + xml_str) + '</bfdCfgSession></bfdCfgSessions>')