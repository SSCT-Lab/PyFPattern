def get_hwtacacs_host_server_cfg(self, **kwargs):
    ' Get hwtacacs host server configure '
    module = kwargs['module']
    hwtacacs_template = module.params['hwtacacs_template']
    hwtacacs_server_host_name = module.params['hwtacacs_server_host_name']
    hwtacacs_server_type = module.params['hwtacacs_server_type']
    hwtacacs_is_secondary_server = ('true' if (module.params['hwtacacs_is_secondary_server'] is True) else 'false')
    hwtacacs_vpn_name = module.params['hwtacacs_vpn_name']
    hwtacacs_is_public_net = ('true' if (module.params['hwtacacs_is_public_net'] is True) else 'false')
    state = module.params['state']
    result = dict()
    result['hwtacacs_server_name_cfg'] = []
    need_cfg = False
    conf_str = (CE_GET_HWTACACS_HOST_SERVER_CFG % hwtacacs_template)
    recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
    if ('<data/>' in recv_xml):
        if (state == 'present'):
            need_cfg = True
    else:
        xml_str = recv_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
        root = ElementTree.fromstring(xml_str)
        hwtacacs_server_name_cfg = root.findall('hwtacacs/hwTacTempCfgs/hwTacTempCfg/hwTacHostSrvCfgs/hwTacHostSrvCfg')
        if hwtacacs_server_name_cfg:
            for tmp in hwtacacs_server_name_cfg:
                tmp_dict = dict()
                for site in tmp:
                    if (site.tag in ['serverHostName', 'serverType', 'isSecondaryServer', 'isPublicNet', 'vpnName']):
                        tmp_dict[site.tag] = site.text
                result['hwtacacs_server_name_cfg'].append(tmp_dict)
        if result['hwtacacs_server_name_cfg']:
            cfg = dict()
            config_list = list()
            if hwtacacs_server_host_name:
                cfg['serverHostName'] = hwtacacs_server_host_name.lower()
            if hwtacacs_server_type:
                cfg['serverType'] = hwtacacs_server_type.lower()
            if hwtacacs_is_secondary_server:
                cfg['isSecondaryServer'] = str(hwtacacs_is_secondary_server).lower()
            if hwtacacs_is_public_net:
                cfg['isPublicNet'] = str(hwtacacs_is_public_net).lower()
            if hwtacacs_vpn_name:
                cfg['vpnName'] = hwtacacs_vpn_name.lower()
            for tmp in result['hwtacacs_server_name_cfg']:
                exist_cfg = dict()
                if hwtacacs_server_host_name:
                    exist_cfg['serverHostName'] = tmp.get('serverHostName').lower()
                if hwtacacs_server_type:
                    exist_cfg['serverType'] = tmp.get('serverType').lower()
                if hwtacacs_is_secondary_server:
                    exist_cfg['isSecondaryServer'] = tmp.get('isSecondaryServer').lower()
                if hwtacacs_is_public_net:
                    exist_cfg['isPublicNet'] = tmp.get('isPublicNet').lower()
                if hwtacacs_vpn_name:
                    exist_cfg['vpnName'] = tmp.get('vpnName').lower()
                config_list.append(exist_cfg)
            if (cfg in config_list):
                if (state == 'present'):
                    need_cfg = False
                else:
                    need_cfg = True
            elif (state == 'present'):
                need_cfg = True
            else:
                need_cfg = False
    result['need_cfg'] = need_cfg
    return result