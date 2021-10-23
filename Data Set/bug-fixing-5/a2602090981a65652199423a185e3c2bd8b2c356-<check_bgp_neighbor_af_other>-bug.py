def check_bgp_neighbor_af_other(self, **kwargs):
    ' check_bgp_neighbor_af_other '
    module = kwargs['module']
    result = dict()
    need_cfg = False
    state = module.params['state']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    remote_address = module.params['remote_address']
    if (state == 'absent'):
        result['need_cfg'] = need_cfg
        return result
    advertise_irb = module.params['advertise_irb']
    if (advertise_irb != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<advertiseIrb></advertiseIrb>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall(('.*<remoteAddress>%s</remoteAddress>\\s*<advertiseIrb>(.*)</advertiseIrb>.*' % remote_address), recv_xml)
            if re_find:
                result['advertise_irb'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != advertise_irb):
                    need_cfg = True
            else:
                need_cfg = True
    advertise_arp = module.params['advertise_arp']
    if (advertise_arp != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<advertiseArp></advertiseArp>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall(('.*<remoteAddress>%s</remoteAddress>\\s*.*<advertiseArp>(.*)</advertiseArp>.*' % remote_address), recv_xml)
            if re_find:
                result['advertise_arp'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != advertise_arp):
                    need_cfg = True
            else:
                need_cfg = True
    advertise_remote_nexthop = module.params['advertise_remote_nexthop']
    if (advertise_remote_nexthop != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<advertiseRemoteNexthop></advertiseRemoteNexthop>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<advertiseRemoteNexthop>(.*)</advertiseRemoteNexthop>.*', recv_xml)
            if re_find:
                result['advertise_remote_nexthop'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != advertise_remote_nexthop):
                    need_cfg = True
            else:
                need_cfg = True
    advertise_community = module.params['advertise_community']
    if (advertise_community != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<advertiseCommunity></advertiseCommunity>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<advertiseCommunity>(.*)</advertiseCommunity>.*', recv_xml)
            if re_find:
                result['advertise_community'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != advertise_community):
                    need_cfg = True
            else:
                need_cfg = True
    advertise_ext_community = module.params['advertise_ext_community']
    if (advertise_ext_community != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<advertiseExtCommunity></advertiseExtCommunity>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<advertiseExtCommunity>(.*)</advertiseExtCommunity>.*', recv_xml)
            if re_find:
                result['advertise_ext_community'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != advertise_ext_community):
                    need_cfg = True
            else:
                need_cfg = True
    discard_ext_community = module.params['discard_ext_community']
    if (discard_ext_community != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<discardExtCommunity></discardExtCommunity>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<discardExtCommunity>(.*)</discardExtCommunity>.*', recv_xml)
            if re_find:
                result['discard_ext_community'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != discard_ext_community):
                    need_cfg = True
            else:
                need_cfg = True
    allow_as_loop_enable = module.params['allow_as_loop_enable']
    if (allow_as_loop_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<allowAsLoopEnable></allowAsLoopEnable>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<allowAsLoopEnable>(.*)</allowAsLoopEnable>.*', recv_xml)
            if re_find:
                result['allow_as_loop_enable'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != allow_as_loop_enable):
                    need_cfg = True
            else:
                need_cfg = True
    allow_as_loop_limit = module.params['allow_as_loop_limit']
    if allow_as_loop_limit:
        if ((int(allow_as_loop_limit) > 10) or (int(allow_as_loop_limit) < 1)):
            module.fail_json(msg=('the value of allow_as_loop_limit %s is out of [1 - 10].' % allow_as_loop_limit))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<allowAsLoopLimit></allowAsLoopLimit>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<allowAsLoopLimit>(.*)</allowAsLoopLimit>.*', recv_xml)
            if re_find:
                result['allow_as_loop_limit'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != allow_as_loop_limit):
                    need_cfg = True
            else:
                need_cfg = True
    keep_all_routes = module.params['keep_all_routes']
    if (keep_all_routes != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<keepAllRoutes></keepAllRoutes>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<keepAllRoutes>(.*)</keepAllRoutes>.*', recv_xml)
            if re_find:
                result['keep_all_routes'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != keep_all_routes):
                    need_cfg = True
            else:
                need_cfg = True
    nexthop_configure = module.params['nexthop_configure']
    if nexthop_configure:
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<nextHopConfigure></nextHopConfigure>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<nextHopConfigure>(.*)</nextHopConfigure>.*', recv_xml)
            if re_find:
                result['nexthop_configure'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != nexthop_configure):
                    need_cfg = True
            else:
                need_cfg = True
    preferred_value = module.params['preferred_value']
    if preferred_value:
        if ((int(preferred_value) > 65535) or (int(preferred_value) < 0)):
            module.fail_json(msg=('the value of preferred_value %s is out of [0 - 65535].' % preferred_value))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<preferredValue></preferredValue>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<preferredValue>(.*)</preferredValue>.*', recv_xml)
            if re_find:
                result['preferred_value'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != preferred_value):
                    need_cfg = True
            else:
                need_cfg = True
    public_as_only = module.params['public_as_only']
    if (public_as_only != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<publicAsOnly></publicAsOnly>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<publicAsOnly>(.*)</publicAsOnly>.*', recv_xml)
            if re_find:
                result['public_as_only'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != public_as_only):
                    need_cfg = True
            else:
                need_cfg = True
    public_as_only_force = module.params['public_as_only_force']
    if (public_as_only_force != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<publicAsOnlyForce></publicAsOnlyForce>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<publicAsOnlyForce>(.*)</publicAsOnlyForce>.*', recv_xml)
            if re_find:
                result['public_as_only_force'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != public_as_only_force):
                    need_cfg = True
            else:
                need_cfg = True
    public_as_only_limited = module.params['public_as_only_limited']
    if (public_as_only_limited != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<publicAsOnlyLimited></publicAsOnlyLimited>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<publicAsOnlyLimited>(.*)</publicAsOnlyLimited>.*', recv_xml)
            if re_find:
                result['public_as_only_limited'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != public_as_only_limited):
                    need_cfg = True
            else:
                need_cfg = True
    public_as_only_replace = module.params['public_as_only_replace']
    if (public_as_only_replace != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<publicAsOnlyReplace></publicAsOnlyReplace>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<publicAsOnlyReplace>(.*)</publicAsOnlyReplace>.*', recv_xml)
            if re_find:
                result['public_as_only_replace'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != public_as_only_replace):
                    need_cfg = True
            else:
                need_cfg = True
    public_as_only_skip_peer_as = module.params['public_as_only_skip_peer_as']
    if (public_as_only_skip_peer_as != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<publicAsOnlySkipPeerAs></publicAsOnlySkipPeerAs>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<publicAsOnlySkipPeerAs>(.*)</publicAsOnlySkipPeerAs>.*', recv_xml)
            if re_find:
                result['public_as_only_skip_peer_as'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != public_as_only_skip_peer_as):
                    need_cfg = True
            else:
                need_cfg = True
    route_limit = module.params['route_limit']
    if route_limit:
        if (int(route_limit) < 1):
            module.fail_json(msg=('the value of route_limit %s is out of [1 - 4294967295].' % route_limit))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<routeLimit></routeLimit>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routeLimit>(.*)</routeLimit>.*', recv_xml)
            if re_find:
                result['route_limit'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != route_limit):
                    need_cfg = True
            else:
                need_cfg = True
    route_limit_percent = module.params['route_limit_percent']
    if route_limit_percent:
        if ((int(route_limit_percent) < 1) or (int(route_limit_percent) > 100)):
            module.fail_json(msg=('Error: The value of route_limit_percent %s is out of [1 - 100].' % route_limit_percent))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<routeLimitPercent></routeLimitPercent>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routeLimitPercent>(.*)</routeLimitPercent>.*', recv_xml)
            if re_find:
                result['route_limit_percent'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != route_limit_percent):
                    need_cfg = True
            else:
                need_cfg = True
    route_limit_type = module.params['route_limit_type']
    if route_limit_type:
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<routeLimitType></routeLimitType>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routeLimitType>(.*)</routeLimitType>.*', recv_xml)
            if re_find:
                result['route_limit_type'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != route_limit_type):
                    need_cfg = True
            else:
                need_cfg = True
    route_limit_idle_timeout = module.params['route_limit_idle_timeout']
    if route_limit_idle_timeout:
        if ((int(route_limit_idle_timeout) < 1) or (int(route_limit_idle_timeout) > 1200)):
            module.fail_json(msg=('Error: The value of route_limit_idle_timeout %s is out of [1 - 1200].' % route_limit_idle_timeout))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<routeLimitIdleTimeout></routeLimitIdleTimeout>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routeLimitIdleTimeout>(.*)</routeLimitIdleTimeout>.*', recv_xml)
            if re_find:
                result['route_limit_idle_timeout'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != route_limit_idle_timeout):
                    need_cfg = True
            else:
                need_cfg = True
    rt_updt_interval = module.params['rt_updt_interval']
    if rt_updt_interval:
        if ((int(rt_updt_interval) < 0) or (int(rt_updt_interval) > 600)):
            module.fail_json(msg=('Error: The value of rt_updt_interval %s is out of [0 - 600].' % rt_updt_interval))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<rtUpdtInterval></rtUpdtInterval>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<rtUpdtInterval>(.*)</rtUpdtInterval>.*', recv_xml)
            if re_find:
                result['rt_updt_interval'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != rt_updt_interval):
                    need_cfg = True
            else:
                need_cfg = True
    redirect_ip = module.params['redirect_ip']
    if (redirect_ip != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<redirectIP></redirectIP>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<redirectIP>(.*)</redirectIP>.*', recv_xml)
            if re_find:
                result['redirect_ip'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != redirect_ip):
                    need_cfg = True
            else:
                need_cfg = True
    redirect_ip_validation = module.params['redirect_ip_validation']
    if (redirect_ip_validation != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<redirectIPVaildation></redirectIPVaildation>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<redirectIPVaildation>(.*)</redirectIPVaildation>.*', recv_xml)
            if re_find:
                result['redirect_ip_validation'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != redirect_ip_validation):
                    need_cfg = True
            else:
                need_cfg = True
    reflect_client = module.params['reflect_client']
    if (reflect_client != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<reflectClient></reflectClient>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<reflectClient>(.*)</reflectClient>.*', recv_xml)
            if re_find:
                result['reflect_client'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != reflect_client):
                    need_cfg = True
            else:
                need_cfg = True
    substitute_as_enable = module.params['substitute_as_enable']
    if (substitute_as_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<substituteAsEnable></substituteAsEnable>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<substituteAsEnable>(.*)</substituteAsEnable>.*', recv_xml)
            if re_find:
                result['substitute_as_enable'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != substitute_as_enable):
                    need_cfg = True
            else:
                need_cfg = True
    import_rt_policy_name = module.params['import_rt_policy_name']
    if import_rt_policy_name:
        if ((len(import_rt_policy_name) < 1) or (len(import_rt_policy_name) > 40)):
            module.fail_json(msg=('Error: The len of import_rt_policy_name %s is out of [1 - 40].' % import_rt_policy_name))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<importRtPolicyName></importRtPolicyName>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<importRtPolicyName>(.*)</importRtPolicyName>.*', recv_xml)
            if re_find:
                result['import_rt_policy_name'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != import_rt_policy_name):
                    need_cfg = True
            else:
                need_cfg = True
    export_rt_policy_name = module.params['export_rt_policy_name']
    if export_rt_policy_name:
        if ((len(export_rt_policy_name) < 1) or (len(export_rt_policy_name) > 40)):
            module.fail_json(msg=('Error: The len of export_rt_policy_name %s is out of [1 - 40].' % export_rt_policy_name))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<exportRtPolicyName></exportRtPolicyName>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<exportRtPolicyName>(.*)</exportRtPolicyName>.*', recv_xml)
            if re_find:
                result['export_rt_policy_name'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != export_rt_policy_name):
                    need_cfg = True
            else:
                need_cfg = True
    import_pref_filt_name = module.params['import_pref_filt_name']
    if import_pref_filt_name:
        if ((len(import_pref_filt_name) < 1) or (len(import_pref_filt_name) > 169)):
            module.fail_json(msg=('Error: The len of import_pref_filt_name %s is out of [1 - 169].' % import_pref_filt_name))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<importPrefFiltName></importPrefFiltName>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<importPrefFiltName>(.*)</importPrefFiltName>.*', recv_xml)
            if re_find:
                result['import_pref_filt_name'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != import_pref_filt_name):
                    need_cfg = True
            else:
                need_cfg = True
    export_pref_filt_name = module.params['export_pref_filt_name']
    if export_pref_filt_name:
        if ((len(export_pref_filt_name) < 1) or (len(export_pref_filt_name) > 169)):
            module.fail_json(msg=('Error: The len of export_pref_filt_name %s is out of [1 - 169].' % export_pref_filt_name))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<exportPrefFiltName></exportPrefFiltName>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<exportPrefFiltName>(.*)</exportPrefFiltName>.*', recv_xml)
            if re_find:
                result['export_pref_filt_name'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != export_pref_filt_name):
                    need_cfg = True
            else:
                need_cfg = True
    import_as_path_filter = module.params['import_as_path_filter']
    if import_as_path_filter:
        if ((int(import_as_path_filter) < 1) or (int(import_as_path_filter) > 256)):
            module.fail_json(msg=('Error: The value of import_as_path_filter %s is out of [1 - 256].' % import_as_path_filter))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<importAsPathFilter></importAsPathFilter>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<importAsPathFilter>(.*)</importAsPathFilter>.*', recv_xml)
            if re_find:
                result['import_as_path_filter'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != import_as_path_filter):
                    need_cfg = True
            else:
                need_cfg = True
    export_as_path_filter = module.params['export_as_path_filter']
    if export_as_path_filter:
        if ((int(export_as_path_filter) < 1) or (int(export_as_path_filter) > 256)):
            module.fail_json(msg=('Error: The value of export_as_path_filter %s is out of [1 - 256].' % export_as_path_filter))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<exportAsPathFilter></exportAsPathFilter>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<exportAsPathFilter>(.*)</exportAsPathFilter>.*', recv_xml)
            if re_find:
                result['export_as_path_filter'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != export_as_path_filter):
                    need_cfg = True
            else:
                need_cfg = True
    import_as_path_name_or_num = module.params['import_as_path_name_or_num']
    if import_as_path_name_or_num:
        if ((len(import_as_path_name_or_num) < 1) or (len(import_as_path_name_or_num) > 51)):
            module.fail_json(msg=('Error: The len of import_as_path_name_or_num %s is out of [1 - 51].' % import_as_path_name_or_num))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<importAsPathNameOrNum></importAsPathNameOrNum>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<importAsPathNameOrNum>(.*)</importAsPathNameOrNum>.*', recv_xml)
            if re_find:
                result['import_as_path_name_or_num'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != import_as_path_name_or_num):
                    need_cfg = True
            else:
                need_cfg = True
    export_as_path_name_or_num = module.params['export_as_path_name_or_num']
    if export_as_path_name_or_num:
        if ((len(export_as_path_name_or_num) < 1) or (len(export_as_path_name_or_num) > 51)):
            module.fail_json(msg=('Error: The len of export_as_path_name_or_num %s is out of [1 - 51].' % export_as_path_name_or_num))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<exportAsPathNameOrNum></exportAsPathNameOrNum>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<exportAsPathNameOrNum>(.*)</exportAsPathNameOrNum>.*', recv_xml)
            if re_find:
                result['export_as_path_name_or_num'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != export_as_path_name_or_num):
                    need_cfg = True
            else:
                need_cfg = True
    import_acl_name_or_num = module.params['import_acl_name_or_num']
    if import_acl_name_or_num:
        if ((len(import_acl_name_or_num) < 1) or (len(import_acl_name_or_num) > 32)):
            module.fail_json(msg=('Error: The len of import_acl_name_or_num %s is out of [1 - 32].' % import_acl_name_or_num))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<importAclNameOrNum></importAclNameOrNum>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<importAclNameOrNum>(.*)</importAclNameOrNum>.*', recv_xml)
            if re_find:
                result['import_acl_name_or_num'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != import_acl_name_or_num):
                    need_cfg = True
            else:
                need_cfg = True
    export_acl_name_or_num = module.params['export_acl_name_or_num']
    if export_acl_name_or_num:
        if ((len(export_acl_name_or_num) < 1) or (len(export_acl_name_or_num) > 32)):
            module.fail_json(msg=('Error: The len of export_acl_name_or_num %s is out of [1 - 32].' % export_acl_name_or_num))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<exportAclNameOrNum></exportAclNameOrNum>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<exportAclNameOrNum>(.*)</exportAclNameOrNum>.*', recv_xml)
            if re_find:
                result['export_acl_name_or_num'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != export_acl_name_or_num):
                    need_cfg = True
            else:
                need_cfg = True
    ipprefix_orf_enable = module.params['ipprefix_orf_enable']
    if (ipprefix_orf_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<ipprefixOrfEnable></ipprefixOrfEnable>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ipprefixOrfEnable>(.*)</ipprefixOrfEnable>.*', recv_xml)
            if re_find:
                result['ipprefix_orf_enable'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != ipprefix_orf_enable):
                    need_cfg = True
            else:
                need_cfg = True
    is_nonstd_ipprefix_mod = module.params['is_nonstd_ipprefix_mod']
    if (is_nonstd_ipprefix_mod != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<isNonstdIpprefixMod></isNonstdIpprefixMod>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<isNonstdIpprefixMod>(.*)</isNonstdIpprefixMod>.*', recv_xml)
            if re_find:
                result['is_nonstd_ipprefix_mod'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != is_nonstd_ipprefix_mod):
                    need_cfg = True
            else:
                need_cfg = True
    orftype = module.params['orftype']
    if orftype:
        if ((int(orftype) < 0) or (int(orftype) > 65535)):
            module.fail_json(msg=('Error: The value of orftype %s is out of [0 - 65535].' % orftype))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<orftype></orftype>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<orftype>(.*)</orftype>.*', recv_xml)
            if re_find:
                result['orftype'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != orftype):
                    need_cfg = True
            else:
                need_cfg = True
    orf_mode = module.params['orf_mode']
    if orf_mode:
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<orfMode></orfMode>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<orfMode>(.*)</orfMode>.*', recv_xml)
            if re_find:
                result['orf_mode'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != orf_mode):
                    need_cfg = True
            else:
                need_cfg = True
    soostring = module.params['soostring']
    if soostring:
        if ((len(soostring) < 3) or (len(soostring) > 21)):
            module.fail_json(msg=('Error: The len of soostring %s is out of [3 - 21].' % soostring))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<soostring></soostring>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<soostring>(.*)</soostring>.*', recv_xml)
            if re_find:
                result['soostring'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != soostring):
                    need_cfg = True
            else:
                need_cfg = True
    default_rt_adv_enable = module.params['default_rt_adv_enable']
    if (default_rt_adv_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<defaultRtAdvEnable></defaultRtAdvEnable>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<defaultRtAdvEnable>(.*)</defaultRtAdvEnable>.*', recv_xml)
            if re_find:
                result['default_rt_adv_enable'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != default_rt_adv_enable):
                    need_cfg = True
            else:
                need_cfg = True
    default_rt_adv_policy = module.params['default_rt_adv_policy']
    if default_rt_adv_policy:
        if ((len(default_rt_adv_policy) < 1) or (len(default_rt_adv_policy) > 40)):
            module.fail_json(msg=('Error: The len of default_rt_adv_policy %s is out of [1 - 40].' % default_rt_adv_policy))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<defaultRtAdvPolicy></defaultRtAdvPolicy>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<defaultRtAdvPolicy>(.*)</defaultRtAdvPolicy>.*', recv_xml)
            if re_find:
                result['default_rt_adv_policy'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != default_rt_adv_policy):
                    need_cfg = True
            else:
                need_cfg = True
    default_rt_match_mode = module.params['default_rt_match_mode']
    if default_rt_match_mode:
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<defaultRtMatchMode></defaultRtMatchMode>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<defaultRtMatchMode>(.*)</defaultRtMatchMode>.*', recv_xml)
            if re_find:
                result['default_rt_match_mode'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != default_rt_match_mode):
                    need_cfg = True
            else:
                need_cfg = True
    add_path_mode = module.params['add_path_mode']
    if add_path_mode:
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<addPathMode></addPathMode>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<addPathMode>(.*)</addPathMode>.*', recv_xml)
            if re_find:
                result['add_path_mode'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != add_path_mode):
                    need_cfg = True
            else:
                need_cfg = True
    adv_add_path_num = module.params['adv_add_path_num']
    if adv_add_path_num:
        if ((int(orftype) < 2) or (int(orftype) > 64)):
            module.fail_json(msg=('Error: The value of adv_add_path_num %s is out of [2 - 64].' % adv_add_path_num))
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<advAddPathNum></advAddPathNum>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<advAddPathNum>(.*)</advAddPathNum>.*', recv_xml)
            if re_find:
                result['adv_add_path_num'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != adv_add_path_num):
                    need_cfg = True
            else:
                need_cfg = True
    origin_as_valid = module.params['origin_as_valid']
    if (origin_as_valid != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<originAsValid></originAsValid>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<originAsValid>(.*)</originAsValid>.*', recv_xml)
            if re_find:
                result['origin_as_valid'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != origin_as_valid):
                    need_cfg = True
            else:
                need_cfg = True
    vpls_enable = module.params['vpls_enable']
    if (vpls_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<vplsEnable></vplsEnable>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<vplsEnable>(.*)</vplsEnable>.*', recv_xml)
            if re_find:
                result['vpls_enable'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != vpls_enable):
                    need_cfg = True
            else:
                need_cfg = True
    vpls_ad_disable = module.params['vpls_ad_disable']
    if (vpls_ad_disable != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<vplsAdDisable></vplsAdDisable>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<vplsAdDisable>(.*)</vplsAdDisable>.*', recv_xml)
            if re_find:
                result['vpls_ad_disable'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != vpls_ad_disable):
                    need_cfg = True
            else:
                need_cfg = True
    update_pkt_standard_compatible = module.params['update_pkt_standard_compatible']
    if (update_pkt_standard_compatible != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address)) + '<updatePktStandardCompatible></updatePktStandardCompatible>') + CE_GET_BGP_PEER_AF_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<updatePktStandardCompatible>(.*)</updatePktStandardCompatible>.*', recv_xml)
            if re_find:
                result['update_pkt_standard_compatible'] = re_find
                result['vrf_name'] = vrf_name
                result['af_type'] = af_type
                if (re_find[0] != update_pkt_standard_compatible):
                    need_cfg = True
            else:
                need_cfg = True
    result['need_cfg'] = need_cfg
    return result