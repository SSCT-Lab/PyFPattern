def check_bgp_af_other_args(self, **kwargs):
    ' check_bgp_af_other_args '
    module = kwargs['module']
    result = dict()
    need_cfg = False
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    max_load_ibgp_num = module.params['max_load_ibgp_num']
    if max_load_ibgp_num:
        if ((int(max_load_ibgp_num) > 65535) or (int(max_load_ibgp_num) < 1)):
            module.fail_json(msg=('Error: The value of max_load_ibgp_num %s is out of [1 - 65535].' % max_load_ibgp_num))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<maxLoadIbgpNum></maxLoadIbgpNum>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<maxLoadIbgpNum>(.*)</maxLoadIbgpNum>.*', recv_xml)
            if re_find:
                result['max_load_ibgp_num'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != max_load_ibgp_num):
                    need_cfg = True
            else:
                need_cfg = True
    ibgp_ecmp_nexthop_changed = module.params['ibgp_ecmp_nexthop_changed']
    if (ibgp_ecmp_nexthop_changed != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ibgpEcmpNexthopChanged></ibgpEcmpNexthopChanged>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ibgpEcmpNexthopChanged>(.*)</ibgpEcmpNexthopChanged>.*', recv_xml)
            if re_find:
                result['ibgp_ecmp_nexthop_changed'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != ibgp_ecmp_nexthop_changed):
                    need_cfg = True
            else:
                need_cfg = True
    max_load_ebgp_num = module.params['max_load_ebgp_num']
    if max_load_ebgp_num:
        if ((int(max_load_ebgp_num) > 65535) or (int(max_load_ebgp_num) < 1)):
            module.fail_json(msg=('Error: The value of max_load_ebgp_num %s is out of [1 - 65535].' % max_load_ebgp_num))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<maxLoadEbgpNum></maxLoadEbgpNum>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<maxLoadEbgpNum>(.*)</maxLoadEbgpNum>.*', recv_xml)
            if re_find:
                result['max_load_ebgp_num'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != max_load_ebgp_num):
                    need_cfg = True
            else:
                need_cfg = True
    ebgp_ecmp_nexthop_changed = module.params['ebgp_ecmp_nexthop_changed']
    if (ebgp_ecmp_nexthop_changed != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ebgpEcmpNexthopChanged></ebgpEcmpNexthopChanged>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ebgpEcmpNexthopChanged>(.*)</ebgpEcmpNexthopChanged>.*', recv_xml)
            if re_find:
                result['ebgp_ecmp_nexthop_changed'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != ebgp_ecmp_nexthop_changed):
                    need_cfg = True
            else:
                need_cfg = True
    maximum_load_balance = module.params['maximum_load_balance']
    if maximum_load_balance:
        if ((int(maximum_load_balance) > 65535) or (int(maximum_load_balance) < 1)):
            module.fail_json(msg=('Error: The value of maximum_load_balance %s is out of [1 - 65535].' % maximum_load_balance))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<maximumLoadBalance></maximumLoadBalance>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<maximumLoadBalance>(.*)</maximumLoadBalance>.*', recv_xml)
            if re_find:
                result['maximum_load_balance'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != maximum_load_balance):
                    need_cfg = True
            else:
                need_cfg = True
    ecmp_nexthop_changed = module.params['ecmp_nexthop_changed']
    if (ecmp_nexthop_changed != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ecmpNexthopChanged></ecmpNexthopChanged>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ecmpNexthopChanged>(.*)</ecmpNexthopChanged>.*', recv_xml)
            if re_find:
                result['ecmp_nexthop_changed'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != ecmp_nexthop_changed):
                    need_cfg = True
            else:
                need_cfg = True
    default_local_pref = module.params['default_local_pref']
    if default_local_pref:
        if (int(default_local_pref) < 0):
            module.fail_json(msg=('Error: The value of default_local_pref %s is out of [0 - 4294967295].' % default_local_pref))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<defaultLocalPref></defaultLocalPref>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<defaultLocalPref>(.*)</defaultLocalPref>.*', recv_xml)
            if re_find:
                result['default_local_pref'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != default_local_pref):
                    need_cfg = True
            else:
                need_cfg = True
    default_med = module.params['default_med']
    if default_med:
        if (int(default_med) < 0):
            module.fail_json(msg=('Error: The value of default_med %s is out of [0 - 4294967295].' % default_med))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<defaultMed></defaultMed>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<defaultMed>(.*)</defaultMed>.*', recv_xml)
            if re_find:
                result['default_med'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != default_med):
                    need_cfg = True
            else:
                need_cfg = True
    default_rt_import_enable = module.params['default_rt_import_enable']
    if (default_rt_import_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<defaultRtImportEnable></defaultRtImportEnable>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<defaultRtImportEnable>(.*)</defaultRtImportEnable>.*', recv_xml)
            if re_find:
                result['default_rt_import_enable'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != default_rt_import_enable):
                    need_cfg = True
            else:
                need_cfg = True
    router_id = module.params['router_id']
    if router_id:
        if (len(router_id) > 255):
            module.fail_json(msg=('Error: The len of router_id %s is out of [0 - 255].' % router_id))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<routerId></routerId>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routerId>(.*)</routerId>.*', recv_xml)
            if re_find:
                result['router_id'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != router_id):
                    need_cfg = True
            else:
                need_cfg = True
    vrf_rid_auto_sel = module.params['vrf_rid_auto_sel']
    if (vrf_rid_auto_sel != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<vrfRidAutoSel></vrfRidAutoSel>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<vrfRidAutoSel>(.*)</vrfRidAutoSel>.*', recv_xml)
            if re_find:
                result['vrf_rid_auto_sel'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != vrf_rid_auto_sel):
                    need_cfg = True
            else:
                need_cfg = True
    nexthop_third_party = module.params['nexthop_third_party']
    if (nexthop_third_party != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<nexthopThirdParty></nexthopThirdParty>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<nexthopThirdParty>(.*)</nexthopThirdParty>.*', recv_xml)
            if re_find:
                result['nexthop_third_party'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != nexthop_third_party):
                    need_cfg = True
            else:
                need_cfg = True
    summary_automatic = module.params['summary_automatic']
    if (summary_automatic != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<summaryAutomatic></summaryAutomatic>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<summaryAutomatic>(.*)</summaryAutomatic>.*', recv_xml)
            if re_find:
                result['summary_automatic'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != summary_automatic):
                    need_cfg = True
            else:
                need_cfg = True
    auto_frr_enable = module.params['auto_frr_enable']
    if (auto_frr_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<autoFrrEnable></autoFrrEnable>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<autoFrrEnable>(.*)</autoFrrEnable>.*', recv_xml)
            if re_find:
                result['auto_frr_enable'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != auto_frr_enable):
                    need_cfg = True
            else:
                need_cfg = True
    load_balancing_as_path_ignore = module.params['load_balancing_as_path_ignore']
    if (load_balancing_as_path_ignore != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<loadBalancingAsPathIgnore></loadBalancingAsPathIgnore>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<loadBalancingAsPathIgnore>(.*)</loadBalancingAsPathIgnore>.*', recv_xml)
            if re_find:
                result['load_balancing_as_path_ignore'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != load_balancing_as_path_ignore):
                    need_cfg = True
            else:
                need_cfg = True
    rib_only_enable = module.params['rib_only_enable']
    if (rib_only_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ribOnlyEnable></ribOnlyEnable>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ribOnlyEnable>(.*)</ribOnlyEnable>.*', recv_xml)
            if re_find:
                result['rib_only_enable'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != rib_only_enable):
                    need_cfg = True
            else:
                need_cfg = True
    rib_only_policy_name = module.params['rib_only_policy_name']
    if rib_only_policy_name:
        if ((len(rib_only_policy_name) > 40) or (len(rib_only_policy_name) < 1)):
            module.fail_json(msg=('Error: The len of rib_only_policy_name %s is out of [1 - 40].' % rib_only_policy_name))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ribOnlyPolicyName></ribOnlyPolicyName>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ribOnlyPolicyName>(.*)</ribOnlyPolicyName>.*', recv_xml)
            if re_find:
                result['rib_only_policy_name'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != rib_only_policy_name):
                    need_cfg = True
            else:
                need_cfg = True
    active_route_advertise = module.params['active_route_advertise']
    if (active_route_advertise != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<activeRouteAdvertise></activeRouteAdvertise>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<activeRouteAdvertise>(.*)</activeRouteAdvertise>.*', recv_xml)
            if re_find:
                result['active_route_advertise'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != active_route_advertise):
                    need_cfg = True
            else:
                need_cfg = True
    as_path_neglect = module.params['as_path_neglect']
    if (as_path_neglect != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<asPathNeglect></asPathNeglect>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<asPathNeglect>(.*)</asPathNeglect>.*', recv_xml)
            if re_find:
                result['as_path_neglect'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != as_path_neglect):
                    need_cfg = True
            else:
                need_cfg = True
    med_none_as_maximum = module.params['med_none_as_maximum']
    if (med_none_as_maximum != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<medNoneAsMaximum></medNoneAsMaximum>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<medNoneAsMaximum>(.*)</medNoneAsMaximum>.*', recv_xml)
            if re_find:
                result['med_none_as_maximum'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != med_none_as_maximum):
                    need_cfg = True
            else:
                need_cfg = True
    router_id_neglect = module.params['router_id_neglect']
    if (router_id_neglect != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<routerIdNeglect></routerIdNeglect>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routerIdNeglect>(.*)</routerIdNeglect>.*', recv_xml)
            if re_find:
                result['router_id_neglect'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != router_id_neglect):
                    need_cfg = True
            else:
                need_cfg = True
    igp_metric_ignore = module.params['igp_metric_ignore']
    if (igp_metric_ignore != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<igpMetricIgnore></igpMetricIgnore>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<igpMetricIgnore>(.*)</igpMetricIgnore>.*', recv_xml)
            if re_find:
                result['igp_metric_ignore'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != igp_metric_ignore):
                    need_cfg = True
            else:
                need_cfg = True
    always_compare_med = module.params['always_compare_med']
    if (always_compare_med != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<alwaysCompareMed></alwaysCompareMed>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<alwaysCompareMed>(.*)</alwaysCompareMed>.*', recv_xml)
            if re_find:
                result['always_compare_med'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != always_compare_med):
                    need_cfg = True
            else:
                need_cfg = True
    determin_med = module.params['determin_med']
    if (determin_med != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<determinMed></determinMed>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<determinMed>(.*)</determinMed>.*', recv_xml)
            if re_find:
                result['determin_med'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != determin_med):
                    need_cfg = True
            else:
                need_cfg = True
    preference_external = module.params['preference_external']
    if preference_external:
        if ((int(preference_external) > 255) or (int(preference_external) < 1)):
            module.fail_json(msg=('Error: The value of preference_external %s is out of [1 - 255].' % preference_external))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<preferenceExternal></preferenceExternal>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<preferenceExternal>(.*)</preferenceExternal>.*', recv_xml)
            if re_find:
                result['preference_external'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != preference_external):
                    need_cfg = True
            else:
                need_cfg = True
    preference_internal = module.params['preference_internal']
    if preference_internal:
        if ((int(preference_internal) > 255) or (int(preference_internal) < 1)):
            module.fail_json(msg=('Error: The value of preference_internal %s is out of [1 - 255].' % preference_internal))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<preferenceInternal></preferenceInternal>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<preferenceInternal>(.*)</preferenceInternal>.*', recv_xml)
            if re_find:
                result['preference_internal'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != preference_internal):
                    need_cfg = True
            else:
                need_cfg = True
    preference_local = module.params['preference_local']
    if preference_local:
        if ((int(preference_local) > 255) or (int(preference_local) < 1)):
            module.fail_json(msg=('Error: The value of preference_local %s is out of [1 - 255].' % preference_local))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<preferenceLocal></preferenceLocal>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<preferenceLocal>(.*)</preferenceLocal>.*', recv_xml)
            if re_find:
                result['preference_local'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != preference_local):
                    need_cfg = True
            else:
                need_cfg = True
    prefrence_policy_name = module.params['prefrence_policy_name']
    if prefrence_policy_name:
        if ((len(prefrence_policy_name) > 40) or (len(prefrence_policy_name) < 1)):
            module.fail_json(msg=('Error: The len of prefrence_policy_name %s is out of [1 - 40].' % prefrence_policy_name))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<prefrencePolicyName></prefrencePolicyName>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<prefrencePolicyName>(.*)</prefrencePolicyName>.*', recv_xml)
            if re_find:
                result['prefrence_policy_name'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != prefrence_policy_name):
                    need_cfg = True
            else:
                need_cfg = True
    reflect_between_client = module.params['reflect_between_client']
    if (reflect_between_client != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<reflectBetweenClient></reflectBetweenClient>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<reflectBetweenClient>(.*)</reflectBetweenClient>.*', recv_xml)
            if re_find:
                result['reflect_between_client'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != reflect_between_client):
                    need_cfg = True
            else:
                need_cfg = True
    reflector_cluster_id = module.params['reflector_cluster_id']
    if reflector_cluster_id:
        if (int(reflector_cluster_id) < 0):
            module.fail_json(msg=('Error: The value of reflector_cluster_id %s is out of [1 - 4294967295].' % reflector_cluster_id))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<reflectorClusterId></reflectorClusterId>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<reflectorClusterId>(.*)</reflectorClusterId>.*', recv_xml)
            if re_find:
                result['reflector_cluster_id'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != reflector_cluster_id):
                    need_cfg = True
            else:
                need_cfg = True
    reflector_cluster_ipv4 = module.params['reflector_cluster_ipv4']
    if reflector_cluster_ipv4:
        if (len(reflector_cluster_ipv4) > 255):
            module.fail_json(msg=('Error: The len of reflector_cluster_ipv4 %s is out of [0 - 255].' % reflector_cluster_ipv4))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<reflectorClusterIpv4></reflectorClusterIpv4>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<reflectorClusterIpv4>(.*)</reflectorClusterIpv4>.*', recv_xml)
            if re_find:
                result['reflector_cluster_ipv4'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != reflector_cluster_ipv4):
                    need_cfg = True
            else:
                need_cfg = True
    rr_filter_number = module.params['rr_filter_number']
    if rr_filter_number:
        if ((len(rr_filter_number) > 51) or (len(rr_filter_number) < 1)):
            module.fail_json(msg=('Error: The len of rr_filter_number %s is out of [1 - 51].' % rr_filter_number))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<rrFilterNumber></rrFilterNumber>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<rrFilterNumber>(.*)</rrFilterNumber>.*', recv_xml)
            if re_find:
                result['rr_filter_number'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != rr_filter_number):
                    need_cfg = True
            else:
                need_cfg = True
    policy_vpn_target = module.params['policy_vpn_target']
    if (policy_vpn_target != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<policyVpnTarget></policyVpnTarget>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<policyVpnTarget>(.*)</policyVpnTarget>.*', recv_xml)
            if re_find:
                result['policy_vpn_target'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != policy_vpn_target):
                    need_cfg = True
            else:
                need_cfg = True
    next_hop_sel_depend_type = module.params['next_hop_sel_depend_type']
    if next_hop_sel_depend_type:
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<nextHopSelDependType></nextHopSelDependType>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<nextHopSelDependType>(.*)</nextHopSelDependType>.*', recv_xml)
            if re_find:
                result['next_hop_sel_depend_type'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != next_hop_sel_depend_type):
                    need_cfg = True
            else:
                need_cfg = True
    nhp_relay_route_policy_name = module.params['nhp_relay_route_policy_name']
    if nhp_relay_route_policy_name:
        if ((len(nhp_relay_route_policy_name) > 40) or (len(nhp_relay_route_policy_name) < 1)):
            module.fail_json(msg=('Error: The len of nhp_relay_route_policy_name %s is out of [1 - 40].' % nhp_relay_route_policy_name))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<nhpRelayRoutePolicyName></nhpRelayRoutePolicyName>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<nhpRelayRoutePolicyName>(.*)</nhpRelayRoutePolicyName>.*', recv_xml)
            if re_find:
                result['nhp_relay_route_policy_name'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != nhp_relay_route_policy_name):
                    need_cfg = True
            else:
                need_cfg = True
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    if (ebgp_if_sensitive != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ebgpIfSensitive></ebgpIfSensitive>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ebgpIfSensitive>(.*)</ebgpIfSensitive>.*', recv_xml)
            if re_find:
                result['ebgp_if_sensitive'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != ebgp_if_sensitive):
                    need_cfg = True
            else:
                need_cfg = True
    reflect_chg_path = module.params['reflect_chg_path']
    if (reflect_chg_path != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<reflectChgPath></reflectChgPath>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<reflectChgPath>(.*)</reflectChgPath>.*', recv_xml)
            if re_find:
                result['reflect_chg_path'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != reflect_chg_path):
                    need_cfg = True
            else:
                need_cfg = True
    add_path_sel_num = module.params['add_path_sel_num']
    if add_path_sel_num:
        if ((int(add_path_sel_num) > 64) or (int(add_path_sel_num) < 2)):
            module.fail_json(msg=('Error: The value of add_path_sel_num %s is out of [2 - 64].' % add_path_sel_num))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<addPathSelNum></addPathSelNum>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<addPathSelNum>(.*)</addPathSelNum>.*', recv_xml)
            if re_find:
                result['add_path_sel_num'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != add_path_sel_num):
                    need_cfg = True
            else:
                need_cfg = True
    route_sel_delay = module.params['route_sel_delay']
    if route_sel_delay:
        if ((int(route_sel_delay) > 3600) or (int(route_sel_delay) < 0)):
            module.fail_json(msg=('Error: The value of route_sel_delay %s is out of [0 - 3600].' % route_sel_delay))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<routeSelDelay></routeSelDelay>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routeSelDelay>(.*)</routeSelDelay>.*', recv_xml)
            if re_find:
                result['route_sel_delay'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != route_sel_delay):
                    need_cfg = True
            else:
                need_cfg = True
    allow_invalid_as = module.params['allow_invalid_as']
    if (allow_invalid_as != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<allowInvalidAs></allowInvalidAs>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<allowInvalidAs>(.*)</allowInvalidAs>.*', recv_xml)
            if re_find:
                result['allow_invalid_as'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != allow_invalid_as):
                    need_cfg = True
            else:
                need_cfg = True
    policy_ext_comm_enable = module.params['policy_ext_comm_enable']
    if (policy_ext_comm_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<policyExtCommEnable></policyExtCommEnable>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<policyExtCommEnable>(.*)</policyExtCommEnable>.*', recv_xml)
            if re_find:
                result['policy_ext_comm_enable'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != policy_ext_comm_enable):
                    need_cfg = True
            else:
                need_cfg = True
    supernet_uni_adv = module.params['supernet_uni_adv']
    if (supernet_uni_adv != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<supernetUniAdv></supernetUniAdv>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<supernetUniAdv>(.*)</supernetUniAdv>.*', recv_xml)
            if re_find:
                result['supernet_uni_adv'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != supernet_uni_adv):
                    need_cfg = True
            else:
                need_cfg = True
    supernet_label_adv = module.params['supernet_label_adv']
    if (supernet_label_adv != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<supernetLabelAdv></supernetLabelAdv>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<supernetLabelAdv>(.*)</supernetLabelAdv>.*', recv_xml)
            if re_find:
                result['supernet_label_adv'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != supernet_label_adv):
                    need_cfg = True
            else:
                need_cfg = True
    ingress_lsp_policy_name = module.params['ingress_lsp_policy_name']
    if ingress_lsp_policy_name:
        if ((len(ingress_lsp_policy_name) > 40) or (len(ingress_lsp_policy_name) < 1)):
            module.fail_json(msg=('Error: The len of ingress_lsp_policy_name %s is out of [1 - 40].' % ingress_lsp_policy_name))
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<ingressLspPolicyName></ingressLspPolicyName>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ingressLspPolicyName>(.*)</ingressLspPolicyName>.*', recv_xml)
            if re_find:
                result['ingress_lsp_policy_name'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != ingress_lsp_policy_name):
                    need_cfg = True
            else:
                need_cfg = True
    originator_prior = module.params['originator_prior']
    if (originator_prior != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<originatorPrior></originatorPrior>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<originatorPrior>(.*)</originatorPrior>.*', recv_xml)
            if re_find:
                result['originator_prior'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != originator_prior):
                    need_cfg = True
            else:
                need_cfg = True
    lowest_priority = module.params['lowest_priority']
    if (lowest_priority != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<lowestPriority></lowestPriority>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<lowestPriority>(.*)</lowestPriority>.*', recv_xml)
            if re_find:
                result['lowest_priority'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != lowest_priority):
                    need_cfg = True
            else:
                need_cfg = True
    relay_delay_enable = module.params['relay_delay_enable']
    if (relay_delay_enable != 'no_use'):
        conf_str = (((CE_GET_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + '<relayDelayEnable></relayDelayEnable>') + CE_GET_BGP_ADDRESS_FAMILY_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<relayDelayEnable>(.*)</relayDelayEnable>.*', recv_xml)
            if re_find:
                result['relay_delay_enable'] = re_find
                result['vrf_name'] = vrf_name
                if (re_find[0] != relay_delay_enable):
                    need_cfg = True
            else:
                need_cfg = True
    result['need_cfg'] = need_cfg
    return result