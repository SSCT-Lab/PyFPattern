def main():
    ' main '
    argument_spec = dict(state=dict(choices=['present', 'absent'], default='present'), vrf_name=dict(type='str', required=True), af_type=dict(choices=['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv6uni', 'ipv6vpn', 'evpn'], required=True), remote_address=dict(type='str', required=True), advertise_irb=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), advertise_arp=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), advertise_remote_nexthop=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), advertise_community=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), advertise_ext_community=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), discard_ext_community=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), allow_as_loop_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), allow_as_loop_limit=dict(type='str'), keep_all_routes=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), nexthop_configure=dict(choices=['null', 'local', 'invariable']), preferred_value=dict(type='str'), public_as_only=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), public_as_only_force=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), public_as_only_limited=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), public_as_only_replace=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), public_as_only_skip_peer_as=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), route_limit=dict(type='str'), route_limit_percent=dict(type='str'), route_limit_type=dict(choices=['noparameter', 'alertOnly', 'idleForever', 'idleTimeout']), route_limit_idle_timeout=dict(type='str'), rt_updt_interval=dict(type='str'), redirect_ip=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), redirect_ip_validation=dict(type='str', default='no_use', choices=['no_use', 'true', 'false'], aliases=['redirect_ip_vaildation']), reflect_client=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), substitute_as_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), import_rt_policy_name=dict(type='str'), export_rt_policy_name=dict(type='str'), import_pref_filt_name=dict(type='str'), export_pref_filt_name=dict(type='str'), import_as_path_filter=dict(type='str'), export_as_path_filter=dict(type='str'), import_as_path_name_or_num=dict(type='str'), export_as_path_name_or_num=dict(type='str'), import_acl_name_or_num=dict(type='str'), export_acl_name_or_num=dict(type='str'), ipprefix_orf_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), is_nonstd_ipprefix_mod=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), orftype=dict(type='str'), orf_mode=dict(choices=['null', 'receive', 'send', 'both']), soostring=dict(type='str'), default_rt_adv_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), default_rt_adv_policy=dict(type='str'), default_rt_match_mode=dict(choices=['null', 'matchall', 'matchany']), add_path_mode=dict(choices=['null', 'receive', 'send', 'both']), adv_add_path_num=dict(type='str'), origin_as_valid=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), vpls_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), vpls_ad_disable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), update_pkt_standard_compatible=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']))
    argument_spec.update(ce_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    changed = False
    proposed = dict()
    existing = dict()
    end_state = dict()
    updates = []
    state = module.params['state']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    remote_address = module.params['remote_address']
    advertise_irb = module.params['advertise_irb']
    advertise_arp = module.params['advertise_arp']
    advertise_remote_nexthop = module.params['advertise_remote_nexthop']
    advertise_community = module.params['advertise_community']
    advertise_ext_community = module.params['advertise_ext_community']
    discard_ext_community = module.params['discard_ext_community']
    allow_as_loop_enable = module.params['allow_as_loop_enable']
    allow_as_loop_limit = module.params['allow_as_loop_limit']
    keep_all_routes = module.params['keep_all_routes']
    nexthop_configure = module.params['nexthop_configure']
    preferred_value = module.params['preferred_value']
    public_as_only = module.params['public_as_only']
    public_as_only_force = module.params['public_as_only_force']
    public_as_only_limited = module.params['public_as_only_limited']
    public_as_only_replace = module.params['public_as_only_replace']
    public_as_only_skip_peer_as = module.params['public_as_only_skip_peer_as']
    route_limit = module.params['route_limit']
    route_limit_percent = module.params['route_limit_percent']
    route_limit_type = module.params['route_limit_type']
    route_limit_idle_timeout = module.params['route_limit_idle_timeout']
    rt_updt_interval = module.params['rt_updt_interval']
    redirect_ip = module.params['redirect_ip']
    redirect_ip_validation = module.params['redirect_ip_validation']
    reflect_client = module.params['reflect_client']
    substitute_as_enable = module.params['substitute_as_enable']
    import_rt_policy_name = module.params['import_rt_policy_name']
    export_rt_policy_name = module.params['export_rt_policy_name']
    import_pref_filt_name = module.params['import_pref_filt_name']
    export_pref_filt_name = module.params['export_pref_filt_name']
    import_as_path_filter = module.params['import_as_path_filter']
    export_as_path_filter = module.params['export_as_path_filter']
    import_as_path_name_or_num = module.params['import_as_path_name_or_num']
    export_as_path_name_or_num = module.params['export_as_path_name_or_num']
    import_acl_name_or_num = module.params['import_acl_name_or_num']
    export_acl_name_or_num = module.params['export_acl_name_or_num']
    ipprefix_orf_enable = module.params['ipprefix_orf_enable']
    is_nonstd_ipprefix_mod = module.params['is_nonstd_ipprefix_mod']
    orftype = module.params['orftype']
    orf_mode = module.params['orf_mode']
    soostring = module.params['soostring']
    default_rt_adv_enable = module.params['default_rt_adv_enable']
    default_rt_adv_policy = module.params['default_rt_adv_policy']
    default_rt_match_mode = module.params['default_rt_match_mode']
    add_path_mode = module.params['add_path_mode']
    adv_add_path_num = module.params['adv_add_path_num']
    origin_as_valid = module.params['origin_as_valid']
    vpls_enable = module.params['vpls_enable']
    vpls_ad_disable = module.params['vpls_ad_disable']
    update_pkt_standard_compatible = module.params['update_pkt_standard_compatible']
    ce_bgp_peer_af_obj = BgpNeighborAf()
    proposed['state'] = state
    if vrf_name:
        proposed['vrf_name'] = vrf_name
    if af_type:
        proposed['af_type'] = af_type
    if remote_address:
        proposed['remote_address'] = remote_address
    if (advertise_irb != 'no_use'):
        proposed['advertise_irb'] = advertise_irb
    if (advertise_arp != 'no_use'):
        proposed['advertise_arp'] = advertise_arp
    if (advertise_remote_nexthop != 'no_use'):
        proposed['advertise_remote_nexthop'] = advertise_remote_nexthop
    if (advertise_community != 'no_use'):
        proposed['advertise_community'] = advertise_community
    if (advertise_ext_community != 'no_use'):
        proposed['advertise_ext_community'] = advertise_ext_community
    if (discard_ext_community != 'no_use'):
        proposed['discard_ext_community'] = discard_ext_community
    if (allow_as_loop_enable != 'no_use'):
        proposed['allow_as_loop_enable'] = allow_as_loop_enable
    if allow_as_loop_limit:
        proposed['allow_as_loop_limit'] = allow_as_loop_limit
    if (keep_all_routes != 'no_use'):
        proposed['keep_all_routes'] = keep_all_routes
    if nexthop_configure:
        proposed['nexthop_configure'] = nexthop_configure
    if preferred_value:
        proposed['preferred_value'] = preferred_value
    if (public_as_only != 'no_use'):
        proposed['public_as_only'] = public_as_only
    if (public_as_only_force != 'no_use'):
        proposed['public_as_only_force'] = public_as_only_force
    if (public_as_only_limited != 'no_use'):
        proposed['public_as_only_limited'] = public_as_only_limited
    if (public_as_only_replace != 'no_use'):
        proposed['public_as_only_replace'] = public_as_only_replace
    if (public_as_only_skip_peer_as != 'no_use'):
        proposed['public_as_only_skip_peer_as'] = public_as_only_skip_peer_as
    if route_limit:
        proposed['route_limit'] = route_limit
    if route_limit_percent:
        proposed['route_limit_percent'] = route_limit_percent
    if route_limit_type:
        proposed['route_limit_type'] = route_limit_type
    if route_limit_idle_timeout:
        proposed['route_limit_idle_timeout'] = route_limit_idle_timeout
    if rt_updt_interval:
        proposed['rt_updt_interval'] = rt_updt_interval
    if (redirect_ip != 'no_use'):
        proposed['redirect_ip'] = redirect_ip
    if (redirect_ip_validation != 'no_use'):
        proposed['redirect_ip_validation'] = redirect_ip_validation
    if (reflect_client != 'no_use'):
        proposed['reflect_client'] = reflect_client
    if (substitute_as_enable != 'no_use'):
        proposed['substitute_as_enable'] = substitute_as_enable
    if import_rt_policy_name:
        proposed['import_rt_policy_name'] = import_rt_policy_name
    if export_rt_policy_name:
        proposed['export_rt_policy_name'] = export_rt_policy_name
    if import_pref_filt_name:
        proposed['import_pref_filt_name'] = import_pref_filt_name
    if export_pref_filt_name:
        proposed['export_pref_filt_name'] = export_pref_filt_name
    if import_as_path_filter:
        proposed['import_as_path_filter'] = import_as_path_filter
    if export_as_path_filter:
        proposed['export_as_path_filter'] = export_as_path_filter
    if import_as_path_name_or_num:
        proposed['import_as_path_name_or_num'] = import_as_path_name_or_num
    if export_as_path_name_or_num:
        proposed['export_as_path_name_or_num'] = export_as_path_name_or_num
    if import_acl_name_or_num:
        proposed['import_acl_name_or_num'] = import_acl_name_or_num
    if export_acl_name_or_num:
        proposed['export_acl_name_or_num'] = export_acl_name_or_num
    if (ipprefix_orf_enable != 'no_use'):
        proposed['ipprefix_orf_enable'] = ipprefix_orf_enable
    if (is_nonstd_ipprefix_mod != 'no_use'):
        proposed['is_nonstd_ipprefix_mod'] = is_nonstd_ipprefix_mod
    if orftype:
        proposed['orftype'] = orftype
    if orf_mode:
        proposed['orf_mode'] = orf_mode
    if soostring:
        proposed['soostring'] = soostring
    if (default_rt_adv_enable != 'no_use'):
        proposed['default_rt_adv_enable'] = default_rt_adv_enable
    if default_rt_adv_policy:
        proposed['default_rt_adv_policy'] = default_rt_adv_policy
    if default_rt_match_mode:
        proposed['default_rt_match_mode'] = default_rt_match_mode
    if add_path_mode:
        proposed['add_path_mode'] = add_path_mode
    if adv_add_path_num:
        proposed['adv_add_path_num'] = adv_add_path_num
    if (origin_as_valid != 'no_use'):
        proposed['origin_as_valid'] = origin_as_valid
    if (vpls_enable != 'no_use'):
        proposed['vpls_enable'] = vpls_enable
    if (vpls_ad_disable != 'no_use'):
        proposed['vpls_ad_disable'] = vpls_ad_disable
    if (update_pkt_standard_compatible != 'no_use'):
        proposed['update_pkt_standard_compatible'] = update_pkt_standard_compatible
    if (not ce_bgp_peer_af_obj):
        module.fail_json(msg='Error: Init module failed.')
    bgp_peer_af_rst = ce_bgp_peer_af_obj.check_bgp_neighbor_af_args(module=module)
    bgp_peer_af_other_rst = ce_bgp_peer_af_obj.check_bgp_neighbor_af_other(module=module)
    exist_tmp = dict()
    for item in bgp_peer_af_rst:
        if (item != 'need_cfg'):
            exist_tmp[item] = bgp_peer_af_rst[item]
    if exist_tmp:
        existing['bgp neighbor af'] = exist_tmp
    exist_tmp = dict()
    for item in bgp_peer_af_other_rst:
        if (item != 'need_cfg'):
            exist_tmp[item] = bgp_peer_af_other_rst[item]
    if exist_tmp:
        existing['bgp neighbor af other'] = exist_tmp
    if (state == 'present'):
        if bgp_peer_af_rst['need_cfg']:
            if ('remote_address' in bgp_peer_af_rst.keys()):
                cmd = ce_bgp_peer_af_obj.merge_bgp_peer_af(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
            else:
                cmd = ce_bgp_peer_af_obj.create_bgp_peer_af(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
        if bgp_peer_af_other_rst['need_cfg']:
            cmd = ce_bgp_peer_af_obj.merge_bgp_peer_af_other(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
    else:
        if bgp_peer_af_rst['need_cfg']:
            cmd = ce_bgp_peer_af_obj.delete_bgp_peer_af(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        if bgp_peer_af_other_rst['need_cfg']:
            pass
    bgp_peer_af_rst = ce_bgp_peer_af_obj.check_bgp_neighbor_af_args(module=module)
    end_tmp = dict()
    for item in bgp_peer_af_rst:
        if (item != 'need_cfg'):
            end_tmp[item] = bgp_peer_af_rst[item]
    if end_tmp:
        end_state['bgp neighbor af'] = end_tmp
    bgp_peer_af_other_rst = ce_bgp_peer_af_obj.check_bgp_neighbor_af_other(module=module)
    end_tmp = dict()
    for item in bgp_peer_af_other_rst:
        if (item != 'need_cfg'):
            end_tmp[item] = bgp_peer_af_other_rst[item]
    if end_tmp:
        end_state['bgp neighbor af other'] = end_tmp
    results = dict()
    results['proposed'] = proposed
    results['existing'] = existing
    results['changed'] = changed
    results['end_state'] = end_state
    results['updates'] = updates
    module.exit_json(**results)