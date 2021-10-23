def config_agent(self):
    'configures sFlow agent'
    xml_str = ''
    if (not self.agent_ip):
        return xml_str
    self.agent_version = get_ip_version(self.agent_ip)
    if (not self.agent_version):
        self.module.fail_json(msg='Error: agent_ip is invalid.')
    if (self.state == 'present'):
        if ((self.agent_ip != self.sflow_dict['agent'].get('ipv4Addr')) and (self.agent_ip != self.sflow_dict['agent'].get('ipv6Addr'))):
            xml_str += '<agents><agent operation="merge">'
            xml_str += ('<family>%s</family>' % self.agent_version)
            if (self.agent_version == 'ipv4'):
                xml_str += ('<ipv4Addr>%s</ipv4Addr>' % self.agent_ip)
                self.updates_cmd.append(('sflow agent ip %s' % self.agent_ip))
            else:
                xml_str += ('<ipv6Addr>%s</ipv6Addr>' % self.agent_ip)
                self.updates_cmd.append(('sflow agent ipv6 %s' % self.agent_ip))
            xml_str += '</agent></agents>'
    else:
        flag = False
        if (self.agent_ip == self.sflow_dict['agent'].get('ipv4Addr')):
            self.updates_cmd.append(('undo sflow agent ip %s' % self.agent_ip))
            flag = True
        elif (self.agent_ip == self.sflow_dict['agent'].get('ipv6Addr')):
            self.updates_cmd.append(('undo sflow agent ipv6 %s' % self.agent_ip))
            flag = True
        if (flag is True):
            xml_str += '<agents><agent operation="delete"></agent></agents>'
    return xml_str