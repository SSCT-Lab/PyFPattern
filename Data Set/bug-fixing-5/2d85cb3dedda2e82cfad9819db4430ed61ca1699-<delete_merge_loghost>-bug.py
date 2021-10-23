def delete_merge_loghost(self):
    'delete loghost ip or dns'
    conf_str = ''
    is_default_vpn = 'false'
    if (self.is_default_vpn is True):
        is_default_vpn = 'true'
    if self.ip_type:
        conf_str = (CE_NC_DELETE_SERVER_IP_INFO_HEADER % (self.ip_type, self.server_ip, self.vrf_name, is_default_vpn))
    elif self.server_domain:
        conf_str = (CE_NC_DELETE_SERVER_DNS_INFO_HEADER % (self.server_domain, self.vrf_name, is_default_vpn))
    if self.level:
        conf_str += ('<level>%s</level>' % self.level)
    if self.server_port:
        conf_str += ('<serverPort>%s</serverPort>' % self.server_port)
    if self.facility:
        conf_str += ('<facility>%s</facility>' % self.facility)
    if self.channel_id:
        conf_str += ('<chnlId>%s</chnlId>' % self.channel_id)
    if self.channel_name:
        conf_str += ('<chnlName>%s</chnlName>' % self.channel_name)
    if self.timestamp:
        conf_str += ('<timestamp>%s</timestamp>' % self.timestamp)
    if self.transport_mode:
        conf_str += ('<transportMode>%s</transportMode>' % self.transport_mode)
    if self.ssl_policy_name:
        conf_str += ('<sslPolicyName>%s</sslPolicyName>' % self.ssl_policy_name)
    if self.source_ip:
        conf_str += ('<sourceIP>%s</sourceIP>' % self.source_ip)
    if self.ip_type:
        conf_str += CE_NC_DELETE_SERVER_IP_INFO_TAIL
    elif self.server_domain:
        conf_str += CE_NC_DELETE_SERVER_DNS_INFO_TAIL
    recv_xml = set_nc_config(self.module, conf_str)
    if ('<ok/>' not in recv_xml):
        self.module.fail_json(msg='Error: Merge server loghost failed.')
    cmd = 'undo info-center loghost'
    if ((self.ip_type == 'ipv4') and self.server_ip):
        cmd += (' %s' % self.server_ip)
    if ((self.ip_type == 'ipv6') and self.server_ip):
        cmd += (' ipv6 %s' % self.server_ip)
    if self.server_domain:
        cmd += (' domain %s' % self.server_domain)
    if self.vrf_name:
        if (self.vrf_name != '_public_'):
            cmd += (' vpn-instance %s' % self.vrf_name)
    if self.level:
        cmd += (' level %s' % self.level)
    if self.server_port:
        cmd += (' port %s' % self.server_port)
    if self.facility:
        cmd += (' facility %s' % self.facility)
    if self.channel_id:
        cmd += (' channel %s' % self.channel_id)
    if self.channel_name:
        cmd += (' channel %s' % self.channel_name)
    if self.timestamp:
        cmd += (' %s' % self.timestamp)
    if self.transport_mode:
        cmd += (' transport %s' % self.transport_mode)
    if self.source_ip:
        cmd += (' source-ip %s' % self.source_ip)
    if self.ssl_policy_name:
        cmd += (' ssl-policy %s' % self.ssl_policy_name)
    self.updates_cmd.append(cmd)
    self.changed = True