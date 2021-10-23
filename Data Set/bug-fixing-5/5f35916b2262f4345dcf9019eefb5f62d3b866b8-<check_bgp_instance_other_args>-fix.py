def check_bgp_instance_other_args(self, **kwargs):
    ' check_bgp_instance_other_args '
    module = kwargs['module']
    state = module.params['state']
    result = dict()
    need_cfg = False
    vrf_name = module.params['vrf_name']
    router_id = module.params['router_id']
    if router_id:
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        if (check_ip_addr(ipaddr=router_id) == FAILED):
            module.fail_json(msg=('Error: The router_id %s is invalid.' % router_id))
        conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<routerId></routerId>') + CE_GET_BGP_INSTANCE_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<routerId>(.*)</routerId>.*', recv_xml)
                if re_find:
                    result['router_id'] = re_find
                    if (re_find[0] != router_id):
                        need_cfg = True
                else:
                    need_cfg = True
        elif ('<data/>' in recv_xml):
            pass
        else:
            re_find = re.findall('.*<routerId>(.*)</routerId>.*', recv_xml)
            if re_find:
                result['router_id'] = re_find
                if (re_find[0] == router_id):
                    need_cfg = True
    vrf_rid_auto_sel = module.params['vrf_rid_auto_sel']
    if (vrf_rid_auto_sel != 'no_use'):
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<vrfRidAutoSel></vrfRidAutoSel>') + CE_GET_BGP_INSTANCE_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<vrfRidAutoSel>(.*)</vrfRidAutoSel>.*', recv_xml)
                if re_find:
                    result['vrf_rid_auto_sel'] = re_find
                    if (re_find[0] != vrf_rid_auto_sel):
                        need_cfg = True
                else:
                    need_cfg = True
    keepalive_time = module.params['keepalive_time']
    if keepalive_time:
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        if ((int(keepalive_time) > 21845) or (int(keepalive_time) < 0)):
            module.fail_json(msg=('keepalive_time %s is out of [0 - 21845].' % keepalive_time))
        else:
            conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<keepaliveTime></keepaliveTime>') + CE_GET_BGP_INSTANCE_TAIL)
            recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
            if (state == 'present'):
                if ('<data/>' in recv_xml):
                    need_cfg = True
                else:
                    re_find = re.findall('.*<keepaliveTime>(.*)</keepaliveTime>.*', recv_xml)
                    if re_find:
                        result['keepalive_time'] = re_find
                        if (re_find[0] != keepalive_time):
                            need_cfg = True
                    else:
                        need_cfg = True
            elif ('<data/>' in recv_xml):
                pass
            else:
                re_find = re.findall('.*<keepaliveTime>(.*)</keepaliveTime>.*', recv_xml)
                if re_find:
                    result['keepalive_time'] = re_find
                    if (re_find[0] == keepalive_time):
                        need_cfg = True
    hold_time = module.params['hold_time']
    if hold_time:
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        if ((int(hold_time) > 65535) or (int(hold_time) < 3)):
            module.fail_json(msg=('hold_time %s is out of [3 - 65535].' % hold_time))
        else:
            conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<holdTime></holdTime>') + CE_GET_BGP_INSTANCE_TAIL)
            recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
            if (state == 'present'):
                if ('<data/>' in recv_xml):
                    need_cfg = True
                else:
                    re_find = re.findall('.*<holdTime>(.*)</holdTime>.*', recv_xml)
                    if re_find:
                        result['hold_time'] = re_find
                        if (re_find[0] != hold_time):
                            need_cfg = True
                    else:
                        need_cfg = True
            elif ('<data/>' in recv_xml):
                pass
            else:
                re_find = re.findall('.*<holdTime>(.*)</holdTime>.*', recv_xml)
                if re_find:
                    result['hold_time'] = re_find
                    if (re_find[0] == hold_time):
                        need_cfg = True
    min_hold_time = module.params['min_hold_time']
    if min_hold_time:
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        if ((int(min_hold_time) != 0) and ((int(min_hold_time) > 65535) or (int(min_hold_time) < 20))):
            module.fail_json(msg=('min_hold_time %s is out of [0, or 20 - 65535].' % min_hold_time))
        else:
            conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<minHoldTime></minHoldTime>') + CE_GET_BGP_INSTANCE_TAIL)
            recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
            if (state == 'present'):
                if ('<data/>' in recv_xml):
                    need_cfg = True
                else:
                    re_find = re.findall('.*<minHoldTime>(.*)</minHoldTime>.*', recv_xml)
                    if re_find:
                        result['min_hold_time'] = re_find
                        if (re_find[0] != min_hold_time):
                            need_cfg = True
                    else:
                        need_cfg = True
            elif ('<data/>' in recv_xml):
                pass
            else:
                re_find = re.findall('.*<minHoldTime>(.*)</minHoldTime>.*', recv_xml)
                if re_find:
                    result['min_hold_time'] = re_find
                    if (re_find[0] == min_hold_time):
                        need_cfg = True
    conn_retry_time = module.params['conn_retry_time']
    if conn_retry_time:
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        if ((int(conn_retry_time) > 65535) or (int(conn_retry_time) < 1)):
            module.fail_json(msg=('conn_retry_time %s is out of [1 - 65535].' % conn_retry_time))
        else:
            conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<connRetryTime></connRetryTime>') + CE_GET_BGP_INSTANCE_TAIL)
            recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
            if (state == 'present'):
                if ('<data/>' in recv_xml):
                    need_cfg = True
                else:
                    re_find = re.findall('.*<connRetryTime>(.*)</connRetryTime>.*', recv_xml)
                    if re_find:
                        result['conn_retry_time'] = re_find
                        if (re_find[0] != conn_retry_time):
                            need_cfg = True
                    else:
                        need_cfg = True
            elif ('<data/>' in recv_xml):
                pass
            else:
                re_find = re.findall('.*<connRetryTime>(.*)</connRetryTime>.*', recv_xml)
                if re_find:
                    result['conn_retry_time'] = re_find
                    if (re_find[0] == conn_retry_time):
                        need_cfg = True
                else:
                    pass
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    if (ebgp_if_sensitive != 'no_use'):
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<ebgpIfSensitive></ebgpIfSensitive>') + CE_GET_BGP_INSTANCE_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<ebgpIfSensitive>(.*)</ebgpIfSensitive>.*', recv_xml)
                if re_find:
                    result['ebgp_if_sensitive'] = re_find
                    if (re_find[0] != ebgp_if_sensitive):
                        need_cfg = True
                else:
                    need_cfg = True
        elif ('<data/>' in recv_xml):
            pass
        else:
            re_find = re.findall('.*<ebgpIfSensitive>(.*)</ebgpIfSensitive>.*', recv_xml)
            if re_find:
                result['ebgp_if_sensitive'] = re_find
                if (re_find[0] == ebgp_if_sensitive):
                    need_cfg = True
            else:
                pass
    default_af_type = module.params['default_af_type']
    if default_af_type:
        if (not vrf_name):
            module.fail_json(msg='Error: Please input vrf_name.')
        conf_str = (((CE_GET_BGP_INSTANCE_HEADER + ('<vrfName>%s</vrfName>' % vrf_name)) + '<defaultAfType></defaultAfType>') + CE_GET_BGP_INSTANCE_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<defaultAfType>(.*)</defaultAfType>.*', recv_xml)
                if re_find:
                    result['default_af_type'] = re_find
                    if (re_find[0] != default_af_type):
                        need_cfg = True
                else:
                    need_cfg = True
        elif ('<data/>' in recv_xml):
            pass
        else:
            re_find = re.findall('.*<defaultAfType>(.*)</defaultAfType>.*', recv_xml)
            if re_find:
                result['default_af_type'] = re_find
                if (re_find[0] == default_af_type):
                    need_cfg = True
            else:
                pass
    result['need_cfg'] = need_cfg
    return result