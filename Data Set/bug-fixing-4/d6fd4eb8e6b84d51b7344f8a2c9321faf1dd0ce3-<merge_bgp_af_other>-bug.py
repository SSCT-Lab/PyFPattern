def merge_bgp_af_other(self, **kwargs):
    ' merge_bgp_af_other '
    module = kwargs['module']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    conf_str = (CE_MERGE_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type))
    cmds = []
    max_load_ibgp_num = module.params['max_load_ibgp_num']
    if max_load_ibgp_num:
        conf_str += ('<maxLoadIbgpNum>%s</maxLoadIbgpNum>' % max_load_ibgp_num)
        cmd = ('maximum load-balancing ibgp %s' % max_load_ibgp_num)
        cmds.append(cmd)
    ibgp_ecmp_nexthop_changed = module.params['ibgp_ecmp_nexthop_changed']
    if (ibgp_ecmp_nexthop_changed != 'no_use'):
        conf_str += ('<ibgpEcmpNexthopChanged>%s</ibgpEcmpNexthopChanged>' % ibgp_ecmp_nexthop_changed)
        if (ibgp_ecmp_nexthop_changed == 'true'):
            cmd = ('maximum load-balancing ibgp %s ecmp-nexthop-changed' % max_load_ibgp_num)
            cmds.append(cmd)
    max_load_ebgp_num = module.params['max_load_ebgp_num']
    if max_load_ebgp_num:
        conf_str += ('<maxLoadEbgpNum>%s</maxLoadEbgpNum>' % max_load_ebgp_num)
        cmd = ('maximum load-balancing ebgp %s' % max_load_ebgp_num)
        cmds.append(cmd)
    ebgp_ecmp_nexthop_changed = module.params['ebgp_ecmp_nexthop_changed']
    if (ebgp_ecmp_nexthop_changed != 'no_use'):
        conf_str += ('<ebgpEcmpNexthopChanged>%s</ebgpEcmpNexthopChanged>' % ebgp_ecmp_nexthop_changed)
        if (ebgp_ecmp_nexthop_changed == 'true'):
            cmd = ('maximum load-balancing ebgp %s ecmp-nexthop-changed' % max_load_ebgp_num)
        else:
            cmd = ('undo maximum load-balancing ebgp %s ecmp-nexthop-changed' % max_load_ebgp_num)
        cmds.append(cmd)
    maximum_load_balance = module.params['maximum_load_balance']
    if maximum_load_balance:
        conf_str += ('<maximumLoadBalance>%s</maximumLoadBalance>' % maximum_load_balance)
        cmd = ('maximum load-balancing %s' % maximum_load_balance)
        cmds.append(cmd)
    ecmp_nexthop_changed = module.params['ecmp_nexthop_changed']
    if (ecmp_nexthop_changed != 'no_use'):
        conf_str += ('<ecmpNexthopChanged>%s</ecmpNexthopChanged>' % ecmp_nexthop_changed)
        if (ecmp_nexthop_changed == 'true'):
            cmd = ('maximum load-balancing %s ecmp-nexthop-changed' % maximum_load_balance)
        else:
            cmd = ('undo maximum load-balancing %s ecmp-nexthop-changed' % maximum_load_balance)
        cmds.append(cmd)
    default_local_pref = module.params['default_local_pref']
    if default_local_pref:
        conf_str += ('<defaultLocalPref>%s</defaultLocalPref>' % default_local_pref)
        cmd = ('default local-preference %s' % default_local_pref)
        cmds.append(cmd)
    default_med = module.params['default_med']
    if default_med:
        conf_str += ('<defaultMed>%s</defaultMed>' % default_med)
        cmd = ('default med %s' % default_med)
        cmds.append(cmd)
    default_rt_import_enable = module.params['default_rt_import_enable']
    if (default_rt_import_enable != 'no_use'):
        conf_str += ('<defaultRtImportEnable>%s</defaultRtImportEnable>' % default_rt_import_enable)
        if (default_rt_import_enable == 'true'):
            cmd = 'default-route imported'
        else:
            cmd = 'undo default-route imported'
        cmds.append(cmd)
    router_id = module.params['router_id']
    if router_id:
        conf_str += ('<routerId>%s</routerId>' % router_id)
        cmd = ('router-id %s' % router_id)
        cmds.append(cmd)
    vrf_rid_auto_sel = module.params['vrf_rid_auto_sel']
    if (vrf_rid_auto_sel != 'no_use'):
        conf_str += ('<vrfRidAutoSel>%s</vrfRidAutoSel>' % vrf_rid_auto_sel)
        if (vrf_rid_auto_sel == 'true'):
            cmd = ('router-id %s vpn-instance auto-select' % router_id)
        else:
            cmd = ('undo router-id %s vpn-instance auto-select' % router_id)
        cmds.append(cmd)
    nexthop_third_party = module.params['nexthop_third_party']
    if (nexthop_third_party != 'no_use'):
        conf_str += ('<nexthopThirdParty>%s</nexthopThirdParty>' % nexthop_third_party)
        if (nexthop_third_party == 'true'):
            cmd = 'nexthop third-party'
        else:
            cmd = 'undo nexthop third-party'
        cmds.append(cmd)
    summary_automatic = module.params['summary_automatic']
    if (summary_automatic != 'no_use'):
        conf_str += ('<summaryAutomatic>%s</summaryAutomatic>' % summary_automatic)
        if (summary_automatic == 'true'):
            cmd = 'summary automatic'
        else:
            cmd = 'undo summary automatic'
        cmds.append(cmd)
    auto_frr_enable = module.params['auto_frr_enable']
    if (auto_frr_enable != 'no_use'):
        conf_str += ('<autoFrrEnable>%s</autoFrrEnable>' % auto_frr_enable)
        if (auto_frr_enable == 'true'):
            cmd = 'auto-frr'
        else:
            cmd = 'undo auto-frr'
        cmds.append(cmd)
    load_balancing_as_path_ignore = module.params['load_balancing_as_path_ignore']
    if (load_balancing_as_path_ignore != 'no_use'):
        conf_str += ('<loadBalancingAsPathIgnore>%s</loadBalancingAsPathIgnore>' % load_balancing_as_path_ignore)
        if (load_balancing_as_path_ignore == 'true'):
            cmd = 'load-balancing as-path-ignore'
        else:
            cmd = 'undo load-balancing as-path-ignore'
        cmds.append(cmd)
    rib_only_enable = module.params['rib_only_enable']
    if (rib_only_enable != 'no_use'):
        conf_str += ('<ribOnlyEnable>%s</ribOnlyEnable>' % rib_only_enable)
        if (rib_only_enable == 'true'):
            cmd = 'routing-table rib-only'
        else:
            cmd = 'undo routing-table rib-only'
        cmds.append(cmd)
    rib_only_policy_name = module.params['rib_only_policy_name']
    if rib_only_policy_name:
        conf_str += ('<ribOnlyPolicyName>%s</ribOnlyPolicyName>' % rib_only_policy_name)
        cmd = ('routing-table rib-only route-policy %s' % rib_only_policy_name)
        cmds.append(cmd)
    active_route_advertise = module.params['active_route_advertise']
    if (active_route_advertise != 'no_use'):
        conf_str += ('<activeRouteAdvertise>%s</activeRouteAdvertise>' % active_route_advertise)
        if (active_route_advertise == 'true'):
            cmd = 'active-route-advertise'
        else:
            cmd = 'undo active-route-advertise'
        cmds.append(cmd)
    as_path_neglect = module.params['as_path_neglect']
    if (as_path_neglect != 'no_use'):
        conf_str += ('<asPathNeglect>%s</asPathNeglect>' % as_path_neglect)
        if (as_path_neglect == 'true'):
            cmd = 'bestroute as-path-ignore'
        else:
            cmd = 'undo bestroute as-path-ignore'
        cmds.append(cmd)
    med_none_as_maximum = module.params['med_none_as_maximum']
    if (med_none_as_maximum != 'no_use'):
        conf_str += ('<medNoneAsMaximum>%s</medNoneAsMaximum>' % med_none_as_maximum)
        if med_none_as_maximum:
            cmd = 'bestroute med-none-as-maximum'
        else:
            cmd = 'undo bestroute med-none-as-maximum'
        cmds.append(cmd)
    router_id_neglect = module.params['router_id_neglect']
    if (router_id_neglect != 'no_use'):
        conf_str += ('<routerIdNeglect>%s</routerIdNeglect>' % router_id_neglect)
        if (router_id_neglect == 'true'):
            cmd = 'bestroute router-id-ignore'
        else:
            cmd = 'undo bestroute router-id-ignore'
        cmds.append(cmd)
    igp_metric_ignore = module.params['igp_metric_ignore']
    if (igp_metric_ignore != 'no_use'):
        conf_str += ('<igpMetricIgnore>%s</igpMetricIgnore>' % igp_metric_ignore)
        if (igp_metric_ignore == 'true'):
            cmd = 'bestroute igp-metric-ignore'
            cmds.append(cmd)
    always_compare_med = module.params['always_compare_med']
    if (always_compare_med != 'no_use'):
        conf_str += ('<alwaysCompareMed>%s</alwaysCompareMed>' % always_compare_med)
        if (always_compare_med == 'true'):
            cmd = 'compare-different-as-med'
            cmds.append(cmd)
    determin_med = module.params['determin_med']
    if (determin_med != 'no_use'):
        conf_str += ('<determinMed>%s</determinMed>' % determin_med)
        if (determin_med == 'true'):
            cmd = 'deterministic-med'
            cmds.append(cmd)
    preference_external = module.params['preference_external']
    if preference_external:
        conf_str += ('<preferenceExternal>%s</preferenceExternal>' % preference_external)
    preference_internal = module.params['preference_internal']
    if preference_internal:
        conf_str += ('<preferenceInternal>%s</preferenceInternal>' % preference_internal)
    preference_local = module.params['preference_local']
    if preference_local:
        conf_str += ('<preferenceLocal>%s</preferenceLocal>' % preference_local)
        cmd = ('preference %s %s %s' % (preference_external, preference_internal, preference_local))
        cmds.append(cmd)
    prefrence_policy_name = module.params['prefrence_policy_name']
    if prefrence_policy_name:
        conf_str += ('<prefrencePolicyName>%s</prefrencePolicyName>' % prefrence_policy_name)
        cmd = ('preference route-policy %s' % prefrence_policy_name)
        cmds.append(cmd)
    reflect_between_client = module.params['reflect_between_client']
    if (reflect_between_client != 'no_use'):
        conf_str += ('<reflectBetweenClient>%s</reflectBetweenClient>' % reflect_between_client)
        if (reflect_between_client == 'true'):
            cmd = 'reflect between-clients'
        else:
            cmd = 'undo reflect between-clients'
        cmds.append(cmd)
    reflector_cluster_id = module.params['reflector_cluster_id']
    if reflector_cluster_id:
        conf_str += ('<reflectorClusterId>%s</reflectorClusterId>' % reflector_cluster_id)
        cmd = ('reflector cluster-id %s' % reflector_cluster_id)
        cmds.append(cmd)
    reflector_cluster_ipv4 = module.params['reflector_cluster_ipv4']
    if reflector_cluster_ipv4:
        conf_str += ('<reflectorClusterIpv4>%s</reflectorClusterIpv4>' % reflector_cluster_ipv4)
        cmd = ('reflector cluster-id %s' % reflector_cluster_ipv4)
        cmds.append(cmd)
    rr_filter_number = module.params['rr_filter_number']
    if rr_filter_number:
        conf_str += ('<rrFilterNumber>%s</rrFilterNumber>' % rr_filter_number)
    policy_vpn_target = module.params['policy_vpn_target']
    if (policy_vpn_target != 'no_use'):
        conf_str += ('<policyVpnTarget>%s</policyVpnTarget>' % policy_vpn_target)
    next_hop_sel_depend_type = module.params['next_hop_sel_depend_type']
    if next_hop_sel_depend_type:
        conf_str += ('<nextHopSelDependType>%s</nextHopSelDependType>' % next_hop_sel_depend_type)
    nhp_relay_route_policy_name = module.params['nhp_relay_route_policy_name']
    if nhp_relay_route_policy_name:
        conf_str += ('<nhpRelayRoutePolicyName>%s</nhpRelayRoutePolicyName>' % nhp_relay_route_policy_name)
        cmd = ('nexthop recursive-lookup route-policy %s' % nhp_relay_route_policy_name)
        cmds.append(cmd)
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    if (ebgp_if_sensitive != 'no_use'):
        conf_str += ('<ebgpIfSensitive>%s</ebgpIfSensitive>' % ebgp_if_sensitive)
        if (ebgp_if_sensitive == 'true'):
            cmd = 'ebgp-interface-sensitive'
        else:
            cmd = 'undo ebgp-interface-sensitive'
        cmds.append(cmd)
    reflect_chg_path = module.params['reflect_chg_path']
    if (reflect_chg_path != 'no_use'):
        conf_str += ('<reflectChgPath>%s</reflectChgPath>' % reflect_chg_path)
        if (reflect_chg_path == 'true'):
            cmd = 'reflect change-path-attribute'
        else:
            cmd = 'undo reflect change-path-attribute'
        cmds.append(cmd)
    add_path_sel_num = module.params['add_path_sel_num']
    if add_path_sel_num:
        conf_str += ('<addPathSelNum>%s</addPathSelNum>' % add_path_sel_num)
        cmd = ('bestroute add-path path-number %s' % add_path_sel_num)
        cmds.append(cmd)
    route_sel_delay = module.params['route_sel_delay']
    if route_sel_delay:
        conf_str += ('<routeSelDelay>%s</routeSelDelay>' % route_sel_delay)
        cmd = ('route-select delay %s' % route_sel_delay)
        cmds.append(cmd)
    allow_invalid_as = module.params['allow_invalid_as']
    if (allow_invalid_as != 'no_use'):
        conf_str += ('<allowInvalidAs>%s</allowInvalidAs>' % allow_invalid_as)
    policy_ext_comm_enable = module.params['policy_ext_comm_enable']
    if (policy_ext_comm_enable != 'no_use'):
        conf_str += ('<policyExtCommEnable>%s</policyExtCommEnable>' % policy_ext_comm_enable)
        if (policy_ext_comm_enable == 'true'):
            cmd = 'ext-community-change enable'
        else:
            cmd = 'undo ext-community-change enable'
        cmds.append(cmd)
    supernet_uni_adv = module.params['supernet_uni_adv']
    if (supernet_uni_adv != 'no_use'):
        conf_str += ('<supernetUniAdv>%s</supernetUniAdv>' % supernet_uni_adv)
        if (supernet_uni_adv == 'true'):
            cmd = 'supernet unicast advertise enable'
        else:
            cmd = 'undo supernet unicast advertise enable'
        cmds.append(cmd)
    supernet_label_adv = module.params['supernet_label_adv']
    if (supernet_label_adv != 'no_use'):
        conf_str += ('<supernetLabelAdv>%s</supernetLabelAdv>' % supernet_label_adv)
        if (supernet_label_adv == 'true'):
            cmd = 'supernet label-route advertise enable'
        else:
            cmd = 'undo supernet label-route advertise enable'
        cmds.append(cmd)
    ingress_lsp_policy_name = module.params['ingress_lsp_policy_name']
    if ingress_lsp_policy_name:
        conf_str += ('<ingressLspPolicyName>%s</ingressLspPolicyName>' % ingress_lsp_policy_name)
        cmd = ('ingress-lsp trigger route-policy %s' % ingress_lsp_policy_name)
        cmds.append(cmd)
    originator_prior = module.params['originator_prior']
    if (originator_prior != 'no_use'):
        conf_str += ('<originatorPrior>%s</originatorPrior>' % originator_prior)
        if (originator_prior == 'true'):
            cmd = 'bestroute routerid-prior-clusterlist'
        else:
            cmd = 'undo bestroute routerid-prior-clusterlist'
        cmds.append(cmd)
    lowest_priority = module.params['lowest_priority']
    if (lowest_priority != 'no_use'):
        conf_str += ('<lowestPriority>%s</lowestPriority>' % lowest_priority)
        if (lowest_priority == 'true'):
            cmd = 'advertise lowest-priority on-startup'
        else:
            cmd = 'undo advertise lowest-priority on-startup'
        cmds.append(cmd)
    relay_delay_enable = module.params['relay_delay_enable']
    if (relay_delay_enable != 'no_use'):
        conf_str += ('<relayDelayEnable>%s</relayDelayEnable>' % relay_delay_enable)
        if (relay_delay_enable == 'true'):
            cmd = 'nexthop recursive-lookup restrain enable'
        else:
            cmd = 'nexthop recursive-lookup restrain disable'
        cmds.append(cmd)
    conf_str += CE_MERGE_BGP_ADDRESS_FAMILY_TAIL
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Merge bgp address family other agrus failed.')
    return cmds