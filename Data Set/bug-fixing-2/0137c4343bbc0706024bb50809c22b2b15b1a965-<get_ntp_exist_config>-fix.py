

def get_ntp_exist_config(self):
    'Get ntp existed configure'
    ntp_config = list()
    conf_str = CE_NC_GET_NTP_CONFIG
    con_obj = get_nc_config(self.module, conf_str)
    if ('<data/>' in con_obj):
        return ntp_config
    xml_str = con_obj.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    ntpsite = root.findall('ntp/ntpUCastCfgs/ntpUCastCfg')
    for nexthop in ntpsite:
        ntp_dict = dict()
        for ele in nexthop:
            if (ele.tag in ['addrFamily', 'vpnName', 'ifName', 'ipv4Addr', 'ipv6Addr', 'type', 'isPreferred', 'keyId']):
                ntp_dict[ele.tag] = ele.text
        ip_addr = ntp_dict['ipv6Addr']
        if (ntp_dict['addrFamily'] == 'IPv4'):
            ip_addr = ntp_dict['ipv4Addr']
        if (ntp_dict['ifName'] is None):
            ntp_dict['ifName'] = ''
        if (ntp_dict['isPreferred'] == 'true'):
            is_preferred = 'enable'
        else:
            is_preferred = 'disable'
        if (self.state == 'present'):
            key_id = (ntp_dict['keyId'] or '')
            cur_ntp_cfg = dict(vpn_name=ntp_dict['vpnName'], source_int=ntp_dict['ifName'].lower(), address=ip_addr, peer_type=ntp_dict['type'], prefer=is_preferred, key_id=key_id)
            exp_ntp_cfg = dict(vpn_name=self.vpn_name, source_int=self.interface.lower(), address=self.address, peer_type=self.peer_type, prefer=self.is_preferred, key_id=self.key_id)
            if (cur_ntp_cfg == exp_ntp_cfg):
                self.conf_exsit = True
        vpn_name = ntp_dict['vpnName']
        if (ntp_dict['vpnName'] == '_public_'):
            vpn_name = None
        if_name = ntp_dict['ifName']
        if (if_name == ''):
            if_name = None
        if (self.peer_type == 'Server'):
            ntp_config.append(dict(vpn_name=vpn_name, source_int=if_name, server=ip_addr, is_preferred=is_preferred, key_id=ntp_dict['keyId']))
        else:
            ntp_config.append(dict(vpn_name=vpn_name, source_int=if_name, peer=ip_addr, is_preferred=is_preferred, key_id=ntp_dict['keyId']))
    return ntp_config
