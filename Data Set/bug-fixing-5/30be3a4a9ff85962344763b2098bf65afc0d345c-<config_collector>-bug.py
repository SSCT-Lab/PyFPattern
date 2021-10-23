def config_collector(self):
    'creates an sFlow collector and sets or modifies optional parameters for the sFlow collector'
    xml_str = ''
    if (not self.collector_id):
        return xml_str
    if ((self.state == 'present') and (not self.collector_ip)):
        return xml_str
    if self.collector_ip:
        self.collector_version = get_ip_version(self.collector_ip)
        if (not self.collector_version):
            self.module.fail_json(msg='Error: collector_ip is invalid.')
    exist_dict = dict()
    for collector in self.sflow_dict['collector']:
        if (collector.get('collectorID') == self.collector_id):
            exist_dict = collector
            break
    change = False
    if (self.state == 'present'):
        if (not exist_dict):
            change = True
        elif (self.collector_version != exist_dict.get('family')):
            change = True
        elif ((self.collector_version == 'ipv4') and (self.collector_ip != exist_dict.get('ipv4Addr'))):
            change = True
        elif ((self.collector_version == 'ipv6') and (self.collector_ip != exist_dict.get('ipv6Addr'))):
            change = True
        elif (self.collector_ip_vpn and (self.collector_ip_vpn != exist_dict.get('vrfName'))):
            change = True
        elif ((not self.collector_ip_vpn) and (exist_dict.get('vrfName') != '_public_')):
            change = True
        elif (self.collector_udp_port and (self.collector_udp_port != exist_dict.get('port'))):
            change = True
        elif ((not self.collector_udp_port) and (exist_dict.get('port') != '6343')):
            change = True
        elif (self.collector_datagram_size and (self.collector_datagram_size != exist_dict.get('datagramSize'))):
            change = True
        elif ((not self.collector_datagram_size) and (exist_dict.get('datagramSize') != '1400')):
            change = True
        elif (self.collector_meth and (self.collector_meth != exist_dict.get('meth'))):
            change = True
        elif ((not self.collector_meth) and exist_dict.get('meth') and (exist_dict.get('meth') != 'meth')):
            change = True
        elif (self.collector_description and (self.collector_description != exist_dict.get('description'))):
            change = True
        elif ((not self.collector_description) and exist_dict.get('description')):
            change = True
        else:
            pass
    else:
        if (not exist_dict):
            return xml_str
        if (self.collector_version and (self.collector_version != exist_dict.get('family'))):
            return xml_str
        if ((self.collector_version == 'ipv4') and (self.collector_ip != exist_dict.get('ipv4Addr'))):
            return xml_str
        if ((self.collector_version == 'ipv6') and (self.collector_ip != exist_dict.get('ipv6Addr'))):
            return xml_str
        if (self.collector_ip_vpn and (self.collector_ip_vpn != exist_dict.get('vrfName'))):
            return xml_str
        if (self.collector_udp_port and (self.collector_udp_port != exist_dict.get('port'))):
            return xml_str
        if (self.collector_datagram_size and (self.collector_datagram_size != exist_dict.get('datagramSize'))):
            return xml_str
        if (self.collector_meth and (self.collector_meth != exist_dict.get('meth'))):
            return xml_str
        if (self.collector_description and (self.collector_description != exist_dict.get('description'))):
            return xml_str
        change = True
    if (not change):
        return xml_str
    if (self.state == 'absent'):
        xml_str += ('<collectors><collector operation="delete"><collectorID>%s</collectorID>' % self.collector_id)
        self.updates_cmd.append(('undo sflow collector %s' % self.collector_id))
    else:
        xml_str += ('<collectors><collector operation="merge"><collectorID>%s</collectorID>' % self.collector_id)
        cmd = ('sflow collector %s' % self.collector_id)
        xml_str += ('<family>%s</family>' % self.collector_version)
        if (self.collector_version == 'ipv4'):
            cmd += (' ip %s' % self.collector_ip)
            xml_str += ('<ipv4Addr>%s</ipv4Addr>' % self.collector_ip)
        else:
            cmd += (' ipv6 %s' % self.collector_ip)
            xml_str += ('<ipv6Addr>%s</ipv6Addr>' % self.collector_ip)
        if self.collector_ip_vpn:
            cmd += (' vpn-instance %s' % self.collector_ip_vpn)
            xml_str += ('<vrfName>%s</vrfName>' % self.collector_ip_vpn)
        if self.collector_datagram_size:
            cmd += (' length %s' % self.collector_datagram_size)
            xml_str += ('<datagramSize>%s</datagramSize>' % self.collector_datagram_size)
        if self.collector_udp_port:
            cmd += (' udp-port %s' % self.collector_udp_port)
            xml_str += ('<port>%s</port>' % self.collector_udp_port)
        if self.collector_description:
            cmd += (' description %s' % self.collector_description)
            xml_str += ('<description>%s</description>' % self.collector_description)
        else:
            xml_str += '<description></description>'
        if self.collector_meth:
            if (self.collector_meth == 'enhanced'):
                cmd += ' enhanced'
            xml_str += ('<meth>%s</meth>' % self.collector_meth)
        self.updates_cmd.append(cmd)
    xml_str += '</collector></collectors>'
    return xml_str