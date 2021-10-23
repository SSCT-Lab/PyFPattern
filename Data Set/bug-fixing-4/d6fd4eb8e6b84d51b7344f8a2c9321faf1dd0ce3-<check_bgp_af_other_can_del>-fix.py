def check_bgp_af_other_can_del(self, **kwargs):
    ' check_bgp_af_other_can_del '
    module = kwargs['module']
    result = dict()
    need_cfg = False
    state = module.params['state']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    router_id = module.params['router_id']
    if router_id:
        if (len(router_id) > 255):
            module.fail_json(msg=('Error: The len of router_id %s is out of [0 - 255].' % router_id))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<routerId></routerId>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<routerId>(.*)</routerId>.*', recv_xml)
                if re_find:
                    if (re_find[0] != router_id):
                        need_cfg = True
                else:
                    need_cfg = True
        elif ('<data/>' in recv_xml):
            pass
        else:
            re_find = re.findall('.*<routerId>(.*)</routerId>.*', recv_xml)
            if re_find:
                if (re_find[0] == router_id):
                    need_cfg = True
            else:
                pass
    determin_med = module.params['determin_med']
    if (determin_med != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<determinMed></determinMed>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<determinMed>(.*)</determinMed>.*', recv_xml)
                if re_find:
                    if (re_find[0] != determin_med):
                        need_cfg = True
                else:
                    need_cfg = True
        elif ('<data/>' in recv_xml):
            pass
        else:
            re_find = re.findall('.*<determinMed>(.*)</determinMed>.*', recv_xml)
            if re_find:
                if (re_find[0] == determin_med):
                    need_cfg = True
            else:
                pass
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    if (ebgp_if_sensitive != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ebgpIfSensitive></ebgpIfSensitive>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<ebgpIfSensitive>(.*)</ebgpIfSensitive>.*', recv_xml)
                if re_find:
                    if (re_find[0] != ebgp_if_sensitive):
                        need_cfg = True
                else:
                    need_cfg = True
        elif ('<data/>' in recv_xml):
            pass
        else:
            re_find = re.findall('.*<ebgpIfSensitive>(.*)</ebgpIfSensitive>.*', recv_xml)
            if re_find:
                if (re_find[0] == ebgp_if_sensitive):
                    need_cfg = True
            else:
                pass
    relay_delay_enable = module.params['relay_delay_enable']
    if (relay_delay_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<relayDelayEnable></relayDelayEnable>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if (state == 'present'):
            if ('<data/>' in recv_xml):
                need_cfg = True
            else:
                re_find = re.findall('.*<relayDelayEnable>(.*)</relayDelayEnable>.*', recv_xml)
                if re_find:
                    if (re_find[0] != relay_delay_enable):
                        need_cfg = True
                else:
                    need_cfg = True
        elif ('<data/>' in recv_xml):
            pass
        else:
            re_find = re.findall('.*<relayDelayEnable>(.*)</relayDelayEnable>.*', recv_xml)
            if re_find:
                if (re_find[0] == relay_delay_enable):
                    need_cfg = True
            else:
                pass
    result['need_cfg'] = need_cfg
    return result