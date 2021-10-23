def check_bgp_af_args(self, **kwargs):
    ' check_bgp_af_args '
    module = kwargs['module']
    result = dict()
    need_cfg = False
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    if vrf_name:
        if ((len(vrf_name) > 31) or (len(vrf_name) == 0)):
            module.fail_json(msg=('Error: The len of vrf_name %s is out of [1 - 31].' % vrf_name))
    else:
        module.fail_json(msg='Error: Please input vrf_name.')
    state = module.params['state']
    af_type = module.params['af_type']
    conf_str = ((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
    recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
    if (state == 'present'):
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<afType>(.*)</afType>.*', recv_xml)
            if re_find:
                result['af_type'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != af_type):
                    need_cfg = True
            else:
                need_cfg = True
    elif ('<data/>' in recv_xml):
        pass
    else:
        re_find = re.findall('.*<afType>(.*)</afType>.*', recv_xml)
        if re_find:
            result['af_type'] = re_find
            result['vrf_name'] = vrf_name
            if (re_find[0] == af_type):
                need_cfg = True
    result['need_cfg'] = need_cfg
    return result