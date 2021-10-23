def check_netconf_args(self, result):
    ' Check invalid netconf args '
    need_cfg = True
    same_flag = True
    delete_flag = False
    result['target_host_info'] = []
    if self.host_name:
        if ((len(self.host_name) > 32) or (len(self.host_name) < 1)):
            self.module.fail_json(msg='Error: The len of host_name is out of [1 - 32].')
        if (self.vpn_name and (self.is_public_net != 'no_use')):
            if (self.is_public_net == 'true'):
                self.module.fail_json(msg='Error: Do not support vpn_name and is_public_net at the same time.')
        conf_str = CE_GET_SNMP_TARGET_HOST_HEADER
        if self.domain:
            conf_str += '<domain></domain>'
        if self.address:
            if (not check_ip_addr(ipaddr=self.address)):
                self.module.fail_json(msg=('Error: The host address [%s] is invalid.' % self.address))
            conf_str += '<address></address>'
        if self.notify_type:
            conf_str += '<notifyType></notifyType>'
        if self.vpn_name:
            if ((len(self.vpn_name) > 31) or (len(self.vpn_name) < 1)):
                self.module.fail_json(msg='Error: The len of vpn_name is out of [1 - 31].')
            conf_str += '<vpnInstanceName></vpnInstanceName>'
        if self.recv_port:
            if ((int(self.recv_port) > 65535) or (int(self.recv_port) < 0)):
                self.module.fail_json(msg='Error: The value of recv_port is out of [0 - 65535].')
            conf_str += '<portNumber></portNumber>'
        if self.security_model:
            conf_str += '<securityModel></securityModel>'
        if self.security_name:
            if ((len(self.security_name) > 32) or (len(self.security_name) < 1)):
                self.module.fail_json(msg='Error: The len of security_name is out of [1 - 32].')
            conf_str += '<securityName></securityName>'
        if self.security_name_v3:
            if ((len(self.security_name_v3) > 32) or (len(self.security_name_v3) < 1)):
                self.module.fail_json(msg='Error: The len of security_name_v3 is out of [1 - 32].')
            conf_str += '<securityNameV3></securityNameV3>'
        if self.security_level:
            conf_str += '<securityLevel></securityLevel>'
        if (self.is_public_net != 'no_use'):
            conf_str += '<isPublicNet></isPublicNet>'
        if self.interface_name:
            if ((len(self.interface_name) > 63) or (len(self.interface_name) < 1)):
                self.module.fail_json(msg='Error: The len of interface_name is out of [1 - 63].')
            find_flag = False
            for item in INTERFACE_TYPE:
                if (item in self.interface_name):
                    find_flag = True
                    break
            if (not find_flag):
                self.module.fail_json(msg='Error: Please input full name of interface_name.')
            conf_str += '<interface-name></interface-name>'
        conf_str += CE_GET_SNMP_TARGET_HOST_TAIL
        recv_xml = self.netconf_get_config(conf_str=conf_str)
        if ('<data/>' in recv_xml):
            if (self.state == 'present'):
                same_flag = False
            else:
                delete_flag = False
        else:
            xml_str = recv_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
            root = ElementTree.fromstring(xml_str)
            target_host_info = root.findall('snmp/targetHosts/targetHost')
            if target_host_info:
                for tmp in target_host_info:
                    tmp_dict = dict()
                    for site in tmp:
                        if (site.tag in ['nmsName', 'domain', 'address', 'notifyType', 'vpnInstanceName', 'portNumber', 'securityModel', 'securityName', 'securityNameV3', 'securityLevel', 'isPublicNet', 'interface-name']):
                            tmp_dict[site.tag] = site.text
                    result['target_host_info'].append(tmp_dict)
            if result['target_host_info']:
                for tmp in result['target_host_info']:
                    same_flag = True
                    if ('nmsName' in tmp.keys()):
                        if (tmp['nmsName'] != self.host_name):
                            same_flag = False
                        else:
                            delete_flag = True
                    if ('domain' in tmp.keys()):
                        if (tmp['domain'] != self.domain):
                            same_flag = False
                    if ('address' in tmp.keys()):
                        if (tmp['address'] != self.address):
                            same_flag = False
                    if ('notifyType' in tmp.keys()):
                        if (tmp['notifyType'] != self.notify_type):
                            same_flag = False
                    if ('vpnInstanceName' in tmp.keys()):
                        if (tmp['vpnInstanceName'] != self.vpn_name):
                            same_flag = False
                    if ('portNumber' in tmp.keys()):
                        if (tmp['portNumber'] != self.recv_port):
                            same_flag = False
                    if ('securityModel' in tmp.keys()):
                        if (tmp['securityModel'] != self.security_model):
                            same_flag = False
                    if ('securityName' in tmp.keys()):
                        if (tmp['securityName'] != self.security_name):
                            same_flag = False
                    if ('securityNameV3' in tmp.keys()):
                        if (tmp['securityNameV3'] != self.security_name_v3):
                            same_flag = False
                    if ('securityLevel' in tmp.keys()):
                        if (tmp['securityLevel'] != self.security_level):
                            same_flag = False
                    if ('isPublicNet' in tmp.keys()):
                        if (tmp['isPublicNet'] != self.is_public_net):
                            same_flag = False
                    if ('interface-name' in tmp.keys()):
                        if (tmp.get('interface-name') is not None):
                            if (tmp['interface-name'].lower() != self.interface_name.lower()):
                                same_flag = False
                        else:
                            same_flag = False
                    if same_flag:
                        break
    if (self.state == 'present'):
        need_cfg = True
        if same_flag:
            need_cfg = False
    else:
        need_cfg = False
        if delete_flag:
            need_cfg = True
    result['need_cfg'] = need_cfg