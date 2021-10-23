def merge_bgp_peer_af_other(self, **kwargs):
    ' merge_bgp_peer_af_other '
    module = kwargs['module']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    remote_address = module.params['remote_address']
    conf_str = (CE_MERGE_BGP_PEER_AF_HEADER % (vrf_name, af_type, remote_address))
    cmds = []
    advertise_irb = module.params['advertise_irb']
    if (advertise_irb != 'no_use'):
        conf_str += ('<advertiseIrb>%s</advertiseIrb>' % advertise_irb)
        if (advertise_irb == 'true'):
            cmd = ('peer %s advertise irb' % remote_address)
        else:
            cmd = ('undo peer %s advertise irb' % remote_address)
        cmds.append(cmd)
    advertise_arp = module.params['advertise_arp']
    if (advertise_arp != 'no_use'):
        conf_str += ('<advertiseArp>%s</advertiseArp>' % advertise_arp)
        if (advertise_arp == 'true'):
            cmd = ('peer %s advertise arp' % remote_address)
        else:
            cmd = ('undo peer %s advertise arp' % remote_address)
        cmds.append(cmd)
    advertise_remote_nexthop = module.params['advertise_remote_nexthop']
    if (advertise_remote_nexthop != 'no_use'):
        conf_str += ('<advertiseRemoteNexthop>%s</advertiseRemoteNexthop>' % advertise_remote_nexthop)
        if (advertise_remote_nexthop == 'true'):
            cmd = ('peer %s advertise remote-nexthop' % remote_address)
        else:
            cmd = ('undo peer %s advertise remote-nexthop' % remote_address)
        cmds.append(cmd)
    advertise_community = module.params['advertise_community']
    if (advertise_community != 'no_use'):
        conf_str += ('<advertiseCommunity>%s</advertiseCommunity>' % advertise_community)
        if (advertise_community == 'true'):
            cmd = ('peer %s advertise-community' % remote_address)
        else:
            cmd = ('undo peer %s advertise-community' % remote_address)
        cmds.append(cmd)
    advertise_ext_community = module.params['advertise_ext_community']
    if (advertise_ext_community != 'no_use'):
        conf_str += ('<advertiseExtCommunity>%s</advertiseExtCommunity>' % advertise_ext_community)
        if (advertise_ext_community == 'true'):
            cmd = ('peer %s advertise-ext-community' % remote_address)
        else:
            cmd = ('undo peer %s advertise-ext-community' % remote_address)
        cmds.append(cmd)
    discard_ext_community = module.params['discard_ext_community']
    if (discard_ext_community != 'no_use'):
        conf_str += ('<discardExtCommunity>%s</discardExtCommunity>' % discard_ext_community)
        if (discard_ext_community == 'true'):
            cmd = ('peer %s discard-ext-community' % remote_address)
        else:
            cmd = ('undo peer %s discard-ext-community' % remote_address)
        cmds.append(cmd)
    allow_as_loop_enable = module.params['allow_as_loop_enable']
    if (allow_as_loop_enable != 'no_use'):
        conf_str += ('<allowAsLoopEnable>%s</allowAsLoopEnable>' % allow_as_loop_enable)
        if (allow_as_loop_enable == 'true'):
            cmd = ('peer %s allow-as-loop' % remote_address)
        else:
            cmd = ('undo peer %s allow-as-loop' % remote_address)
        cmds.append(cmd)
    allow_as_loop_limit = module.params['allow_as_loop_limit']
    if allow_as_loop_limit:
        conf_str += ('<allowAsLoopLimit>%s</allowAsLoopLimit>' % allow_as_loop_limit)
        if (allow_as_loop_enable == 'true'):
            cmd = ('peer %s allow-as-loop %s' % (remote_address, allow_as_loop_limit))
        else:
            cmd = ('undo peer %s allow-as-loop' % remote_address)
        cmds.append(cmd)
    keep_all_routes = module.params['keep_all_routes']
    if (keep_all_routes != 'no_use'):
        conf_str += ('<keepAllRoutes>%s</keepAllRoutes>' % keep_all_routes)
        if (keep_all_routes == 'true'):
            cmd = ('peer %s keep-all-routes' % remote_address)
        else:
            cmd = ('undo peer %s keep-all-routes' % remote_address)
        cmds.append(cmd)
    nexthop_configure = module.params['nexthop_configure']
    if nexthop_configure:
        conf_str += ('<nextHopConfigure>%s</nextHopConfigure>' % nexthop_configure)
        if (nexthop_configure == 'local'):
            cmd = ('peer %s next-hop-local' % remote_address)
            cmds.append(cmd)
        elif (nexthop_configure == 'invariable'):
            cmd = ('peer %s next-hop-invariable' % remote_address)
            cmds.append(cmd)
    preferred_value = module.params['preferred_value']
    if preferred_value:
        conf_str += ('<preferredValue>%s</preferredValue>' % preferred_value)
        cmd = ('peer %s preferred-value %s' % (remote_address, preferred_value))
        cmds.append(cmd)
    public_as_only = module.params['public_as_only']
    if (public_as_only != 'no_use'):
        conf_str += ('<publicAsOnly>%s</publicAsOnly>' % public_as_only)
        if (public_as_only == 'true'):
            cmd = ('peer %s public-as-only' % remote_address)
        else:
            cmd = ('undo peer %s public-as-only' % remote_address)
        cmds.append(cmd)
    public_as_only_force = module.params['public_as_only_force']
    if (public_as_only_force != 'no_use'):
        conf_str += ('<publicAsOnlyForce>%s</publicAsOnlyForce>' % public_as_only_force)
        if (public_as_only_force == 'true'):
            cmd = ('peer %s public-as-only force' % remote_address)
        else:
            cmd = ('undo peer %s public-as-only force' % remote_address)
        cmds.append(cmd)
    public_as_only_limited = module.params['public_as_only_limited']
    if (public_as_only_limited != 'no_use'):
        conf_str += ('<publicAsOnlyLimited>%s</publicAsOnlyLimited>' % public_as_only_limited)
        if (public_as_only_limited == 'true'):
            cmd = ('peer %s public-as-only limited' % remote_address)
        else:
            cmd = ('undo peer %s public-as-only limited' % remote_address)
        cmds.append(cmd)
    public_as_only_replace = module.params['public_as_only_replace']
    if (public_as_only_replace != 'no_use'):
        conf_str += ('<publicAsOnlyReplace>%s</publicAsOnlyReplace>' % public_as_only_replace)
        if (public_as_only_replace == 'true'):
            cmd = ('peer %s public-as-only force replace' % remote_address)
        else:
            cmd = ('undo peer %s public-as-only force replace' % remote_address)
        cmds.append(cmd)
    public_as_only_skip_peer_as = module.params['public_as_only_skip_peer_as']
    if (public_as_only_skip_peer_as != 'no_use'):
        conf_str += ('<publicAsOnlySkipPeerAs>%s</publicAsOnlySkipPeerAs>' % public_as_only_skip_peer_as)
        if (public_as_only_skip_peer_as == 'true'):
            cmd = ('peer %s public-as-only force include-peer-as' % remote_address)
        else:
            cmd = ('undo peer %s public-as-only force include-peer-as' % remote_address)
        cmds.append(cmd)
    route_limit = module.params['route_limit']
    if route_limit:
        conf_str += ('<routeLimit>%s</routeLimit>' % route_limit)
        cmd = ('peer %s route-limit %s' % (remote_address, route_limit))
        cmds.append(cmd)
    route_limit_percent = module.params['route_limit_percent']
    if route_limit_percent:
        conf_str += ('<routeLimitPercent>%s</routeLimitPercent>' % route_limit_percent)
        cmd = ('peer %s route-limit %s %s' % (remote_address, route_limit, route_limit_percent))
        cmds.append(cmd)
    route_limit_type = module.params['route_limit_type']
    if route_limit_type:
        conf_str += ('<routeLimitType>%s</routeLimitType>' % route_limit_type)
        if (route_limit_type == 'alertOnly'):
            cmd = ('peer %s route-limit %s %s alert-only' % (remote_address, route_limit, route_limit_percent))
            cmds.append(cmd)
        elif (route_limit_type == 'idleForever'):
            cmd = ('peer %s route-limit %s %s idle-forever' % (remote_address, route_limit, route_limit_percent))
            cmds.append(cmd)
        elif (route_limit_type == 'idleTimeout'):
            cmd = ('peer %s route-limit %s %s idle-timeout' % (remote_address, route_limit, route_limit_percent))
            cmds.append(cmd)
    route_limit_idle_timeout = module.params['route_limit_idle_timeout']
    if route_limit_idle_timeout:
        conf_str += ('<routeLimitIdleTimeout>%s</routeLimitIdleTimeout>' % route_limit_idle_timeout)
        cmd = ('peer %s route-limit %s %s idle-timeout %s' % (remote_address, route_limit, route_limit_percent, route_limit_idle_timeout))
        cmds.append(cmd)
    rt_updt_interval = module.params['rt_updt_interval']
    if rt_updt_interval:
        conf_str += ('<rtUpdtInterval>%s</rtUpdtInterval>' % rt_updt_interval)
        cmd = ('peer %s route-update-interval %s' % (remote_address, rt_updt_interval))
        cmds.append(cmd)
    redirect_ip = module.params['redirect_ip']
    if (redirect_ip != 'no_use'):
        conf_str += ('<redirectIP>%s</redirectIP>' % redirect_ip)
    redirect_ip_validation = module.params['redirect_ip_validation']
    if (redirect_ip_validation != 'no_use'):
        conf_str += ('<redirectIPVaildation>%s</redirectIPVaildation>' % redirect_ip_validation)
    reflect_client = module.params['reflect_client']
    if (reflect_client != 'no_use'):
        conf_str += ('<reflectClient>%s</reflectClient>' % reflect_client)
        if (reflect_client == 'true'):
            cmd = ('peer %s reflect-client' % remote_address)
        else:
            cmd = ('undo peer %s reflect-client' % remote_address)
        cmds.append(cmd)
    substitute_as_enable = module.params['substitute_as_enable']
    if (substitute_as_enable != 'no_use'):
        conf_str += ('<substituteAsEnable>%s</substituteAsEnable>' % substitute_as_enable)
        if (substitute_as_enable == 'true'):
            cmd = ('peer %s substitute-as' % remote_address)
        else:
            cmd = ('undo peer %s substitute-as' % remote_address)
        cmds.append(cmd)
    import_rt_policy_name = module.params['import_rt_policy_name']
    if import_rt_policy_name:
        conf_str += ('<importRtPolicyName>%s</importRtPolicyName>' % import_rt_policy_name)
        cmd = ('peer %s route-policy %s import' % (remote_address, import_rt_policy_name))
        cmds.append(cmd)
    export_rt_policy_name = module.params['export_rt_policy_name']
    if export_rt_policy_name:
        conf_str += ('<exportRtPolicyName>%s</exportRtPolicyName>' % export_rt_policy_name)
        cmd = ('peer %s route-policy %s export' % (remote_address, export_rt_policy_name))
        cmds.append(cmd)
    import_pref_filt_name = module.params['import_pref_filt_name']
    if import_pref_filt_name:
        conf_str += ('<importPrefFiltName>%s</importPrefFiltName>' % import_pref_filt_name)
        cmd = ('peer %s filter-policy %s import' % (remote_address, import_pref_filt_name))
        cmds.append(cmd)
    export_pref_filt_name = module.params['export_pref_filt_name']
    if export_pref_filt_name:
        conf_str += ('<exportPrefFiltName>%s</exportPrefFiltName>' % export_pref_filt_name)
        cmd = ('peer %s filter-policy %s export' % (remote_address, export_pref_filt_name))
        cmds.append(cmd)
    import_as_path_filter = module.params['import_as_path_filter']
    if import_as_path_filter:
        conf_str += ('<importAsPathFilter>%s</importAsPathFilter>' % import_as_path_filter)
        cmd = ('peer %s as-path-filter %s import' % (remote_address, import_as_path_filter))
        cmds.append(cmd)
    export_as_path_filter = module.params['export_as_path_filter']
    if export_as_path_filter:
        conf_str += ('<exportAsPathFilter>%s</exportAsPathFilter>' % export_as_path_filter)
        cmd = ('peer %s as-path-filter %s export' % (remote_address, export_as_path_filter))
        cmds.append(cmd)
    import_as_path_name_or_num = module.params['import_as_path_name_or_num']
    if import_as_path_name_or_num:
        conf_str += ('<importAsPathNameOrNum>%s</importAsPathNameOrNum>' % import_as_path_name_or_num)
        cmd = ('peer %s as-path-filter %s import' % (remote_address, import_as_path_name_or_num))
        cmds.append(cmd)
    export_as_path_name_or_num = module.params['export_as_path_name_or_num']
    if export_as_path_name_or_num:
        conf_str += ('<exportAsPathNameOrNum>%s</exportAsPathNameOrNum>' % export_as_path_name_or_num)
        cmd = ('peer %s as-path-filter %s export' % (remote_address, export_as_path_name_or_num))
        cmds.append(cmd)
    import_acl_name_or_num = module.params['import_acl_name_or_num']
    if import_acl_name_or_num:
        conf_str += ('<importAclNameOrNum>%s</importAclNameOrNum>' % import_acl_name_or_num)
        cmd = ('peer %s filter-policy %s import' % (remote_address, import_acl_name_or_num))
        cmds.append(cmd)
    export_acl_name_or_num = module.params['export_acl_name_or_num']
    if export_acl_name_or_num:
        conf_str += ('<exportAclNameOrNum>%s</exportAclNameOrNum>' % export_acl_name_or_num)
        cmd = ('peer %s filter-policy %s export' % (remote_address, export_acl_name_or_num))
        cmds.append(cmd)
    ipprefix_orf_enable = module.params['ipprefix_orf_enable']
    if (ipprefix_orf_enable != 'no_use'):
        conf_str += ('<ipprefixOrfEnable>%s</ipprefixOrfEnable>' % ipprefix_orf_enable)
        if (ipprefix_orf_enable == 'true'):
            cmd = ('peer %s capability-advertise orf ip-prefix' % remote_address)
        else:
            cmd = ('undo peer %s capability-advertise orf ip-prefix' % remote_address)
        cmds.append(cmd)
    is_nonstd_ipprefix_mod = module.params['is_nonstd_ipprefix_mod']
    if (is_nonstd_ipprefix_mod != 'no_use'):
        conf_str += ('<isNonstdIpprefixMod>%s</isNonstdIpprefixMod>' % is_nonstd_ipprefix_mod)
        if (is_nonstd_ipprefix_mod == 'true'):
            if (ipprefix_orf_enable == 'true'):
                cmd = ('peer %s capability-advertise orf non-standard-compatible' % remote_address)
            else:
                cmd = ('undo peer %s capability-advertise orf non-standard-compatible' % remote_address)
            cmds.append(cmd)
        else:
            if (ipprefix_orf_enable == 'true'):
                cmd = ('peer %s capability-advertise orf' % remote_address)
            else:
                cmd = ('undo peer %s capability-advertise orf' % remote_address)
            cmds.append(cmd)
    orftype = module.params['orftype']
    if orftype:
        conf_str += ('<orftype>%s</orftype>' % orftype)
    orf_mode = module.params['orf_mode']
    if orf_mode:
        conf_str += ('<orfMode>%s</orfMode>' % orf_mode)
        if (ipprefix_orf_enable == 'true'):
            cmd = ('peer %s capability-advertise orf ip-prefix %s' % (remote_address, orf_mode))
        else:
            cmd = ('undo peer %s capability-advertise orf ip-prefix %s' % (remote_address, orf_mode))
        cmds.append(cmd)
    soostring = module.params['soostring']
    if soostring:
        conf_str += ('<soostring>%s</soostring>' % soostring)
        cmd = ('peer %s soo %s' % (remote_address, soostring))
        cmds.append(cmd)
    cmd = ''
    default_rt_adv_enable = module.params['default_rt_adv_enable']
    if (default_rt_adv_enable != 'no_use'):
        conf_str += ('<defaultRtAdvEnable>%s</defaultRtAdvEnable>' % default_rt_adv_enable)
        if (default_rt_adv_enable == 'true'):
            cmd += ('peer %s default-route-advertise' % remote_address)
        else:
            cmd += ('undo peer %s default-route-advertise' % remote_address)
        cmds.append(cmd)
    default_rt_adv_policy = module.params['default_rt_adv_policy']
    if default_rt_adv_policy:
        conf_str += ('<defaultRtAdvPolicy>%s</defaultRtAdvPolicy>' % default_rt_adv_policy)
        cmd = (' route-policy %s' % default_rt_adv_policy)
        cmds.append(cmd)
    default_rt_match_mode = module.params['default_rt_match_mode']
    if default_rt_match_mode:
        conf_str += ('<defaultRtMatchMode>%s</defaultRtMatchMode>' % default_rt_match_mode)
        if (default_rt_match_mode == 'matchall'):
            cmd += ' conditional-route-match-all'
        elif (default_rt_match_mode == 'matchany'):
            cmd += ' conditional-route-match-any'
        if cmd:
            cmds.append(cmd)
    add_path_mode = module.params['add_path_mode']
    if add_path_mode:
        conf_str += ('<addPathMode>%s</addPathMode>' % add_path_mode)
        if (add_path_mode == 'receive'):
            cmd += ' add-path receive'
        elif (add_path_mode == 'send'):
            cmd += ' add-path send'
        elif (add_path_mode == 'both'):
            cmd += ' add-path both'
        if cmd:
            cmds.append(cmd)
    adv_add_path_num = module.params['adv_add_path_num']
    if adv_add_path_num:
        conf_str += ('<advAddPathNum>%s</advAddPathNum>' % adv_add_path_num)
        cmd += (' advertise add-path path-number %s' % adv_add_path_num)
        if cmd:
            cmds.append(cmd)
    origin_as_valid = module.params['origin_as_valid']
    if (origin_as_valid != 'no_use'):
        conf_str += ('<originAsValid>%s</originAsValid>' % origin_as_valid)
    vpls_enable = module.params['vpls_enable']
    if (vpls_enable != 'no_use'):
        conf_str += ('<vplsEnable>%s</vplsEnable>' % vpls_enable)
    vpls_ad_disable = module.params['vpls_ad_disable']
    if (vpls_ad_disable != 'no_use'):
        conf_str += ('<vplsAdDisable>%s</vplsAdDisable>' % vpls_ad_disable)
    update_pkt_standard_compatible = module.params['update_pkt_standard_compatible']
    if (update_pkt_standard_compatible != 'no_use'):
        conf_str += ('<updatePktStandardCompatible>%s</updatePktStandardCompatible>' % update_pkt_standard_compatible)
    conf_str += CE_MERGE_BGP_PEER_AF_TAIL
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Merge bgp peer address family other failed.')
    return cmds