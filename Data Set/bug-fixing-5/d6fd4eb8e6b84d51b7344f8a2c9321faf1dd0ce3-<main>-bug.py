def main():
    ' main '
    argument_spec = dict(state=dict(choices=['present', 'absent'], default='present'), vrf_name=dict(type='str', required=True), af_type=dict(choices=['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv6uni', 'ipv6vpn', 'evpn'], required=True), max_load_ibgp_num=dict(type='str'), ibgp_ecmp_nexthop_changed=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), max_load_ebgp_num=dict(type='str'), ebgp_ecmp_nexthop_changed=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), maximum_load_balance=dict(type='str'), ecmp_nexthop_changed=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), default_local_pref=dict(type='str'), default_med=dict(type='str'), default_rt_import_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), router_id=dict(type='str'), vrf_rid_auto_sel=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), nexthop_third_party=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), summary_automatic=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), auto_frr_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), load_balancing_as_path_ignore=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), rib_only_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), rib_only_policy_name=dict(type='str'), active_route_advertise=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), as_path_neglect=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), med_none_as_maximum=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), router_id_neglect=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), igp_metric_ignore=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), always_compare_med=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), determin_med=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), preference_external=dict(type='str'), preference_internal=dict(type='str'), preference_local=dict(type='str'), prefrence_policy_name=dict(type='str'), reflect_between_client=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), reflector_cluster_id=dict(type='str'), reflector_cluster_ipv4=dict(type='str'), rr_filter_number=dict(type='str'), policy_vpn_target=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), next_hop_sel_depend_type=dict(choices=['default', 'dependTunnel', 'dependIp']), nhp_relay_route_policy_name=dict(type='str'), ebgp_if_sensitive=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), reflect_chg_path=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), add_path_sel_num=dict(type='str'), route_sel_delay=dict(type='str'), allow_invalid_as=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), policy_ext_comm_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), supernet_uni_adv=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), supernet_label_adv=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), ingress_lsp_policy_name=dict(type='str'), originator_prior=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), lowest_priority=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), relay_delay_enable=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), import_protocol=dict(choices=['direct', 'ospf', 'isis', 'static', 'rip', 'ospfv3', 'ripng']), import_process_id=dict(type='str'), network_address=dict(type='str'), mask_len=dict(type='str'))
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
    max_load_ibgp_num = module.params['max_load_ibgp_num']
    ibgp_ecmp_nexthop_changed = module.params['ibgp_ecmp_nexthop_changed']
    max_load_ebgp_num = module.params['max_load_ebgp_num']
    ebgp_ecmp_nexthop_changed = module.params['ebgp_ecmp_nexthop_changed']
    maximum_load_balance = module.params['maximum_load_balance']
    ecmp_nexthop_changed = module.params['ecmp_nexthop_changed']
    default_local_pref = module.params['default_local_pref']
    default_med = module.params['default_med']
    default_rt_import_enable = module.params['default_rt_import_enable']
    router_id = module.params['router_id']
    vrf_rid_auto_sel = module.params['vrf_rid_auto_sel']
    nexthop_third_party = module.params['nexthop_third_party']
    summary_automatic = module.params['summary_automatic']
    auto_frr_enable = module.params['auto_frr_enable']
    load_balancing_as_path_ignore = module.params['load_balancing_as_path_ignore']
    rib_only_enable = module.params['rib_only_enable']
    rib_only_policy_name = module.params['rib_only_policy_name']
    active_route_advertise = module.params['active_route_advertise']
    as_path_neglect = module.params['as_path_neglect']
    med_none_as_maximum = module.params['med_none_as_maximum']
    router_id_neglect = module.params['router_id_neglect']
    igp_metric_ignore = module.params['igp_metric_ignore']
    always_compare_med = module.params['always_compare_med']
    determin_med = module.params['determin_med']
    preference_external = module.params['preference_external']
    preference_internal = module.params['preference_internal']
    preference_local = module.params['preference_local']
    prefrence_policy_name = module.params['prefrence_policy_name']
    reflect_between_client = module.params['reflect_between_client']
    reflector_cluster_id = module.params['reflector_cluster_id']
    reflector_cluster_ipv4 = module.params['reflector_cluster_ipv4']
    rr_filter_number = module.params['rr_filter_number']
    policy_vpn_target = module.params['policy_vpn_target']
    next_hop_sel_depend_type = module.params['next_hop_sel_depend_type']
    nhp_relay_route_policy_name = module.params['nhp_relay_route_policy_name']
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    reflect_chg_path = module.params['reflect_chg_path']
    add_path_sel_num = module.params['add_path_sel_num']
    route_sel_delay = module.params['route_sel_delay']
    allow_invalid_as = module.params['allow_invalid_as']
    policy_ext_comm_enable = module.params['policy_ext_comm_enable']
    supernet_uni_adv = module.params['supernet_uni_adv']
    supernet_label_adv = module.params['supernet_label_adv']
    ingress_lsp_policy_name = module.params['ingress_lsp_policy_name']
    originator_prior = module.params['originator_prior']
    lowest_priority = module.params['lowest_priority']
    relay_delay_enable = module.params['relay_delay_enable']
    import_protocol = module.params['import_protocol']
    import_process_id = module.params['import_process_id']
    network_address = module.params['network_address']
    mask_len = module.params['mask_len']
    ce_bgp_af_obj = BgpAf()
    if (not ce_bgp_af_obj):
        module.fail_json(msg='Error: Init module failed.')
    proposed['state'] = state
    if vrf_name:
        proposed['vrf_name'] = vrf_name
    if af_type:
        proposed['af_type'] = af_type
    if max_load_ibgp_num:
        proposed['max_load_ibgp_num'] = max_load_ibgp_num
    if (ibgp_ecmp_nexthop_changed != 'no_use'):
        proposed['ibgp_ecmp_nexthop_changed'] = ibgp_ecmp_nexthop_changed
    if max_load_ebgp_num:
        proposed['max_load_ebgp_num'] = max_load_ebgp_num
    if (ebgp_ecmp_nexthop_changed != 'no_use'):
        proposed['ebgp_ecmp_nexthop_changed'] = ebgp_ecmp_nexthop_changed
    if maximum_load_balance:
        proposed['maximum_load_balance'] = maximum_load_balance
    if (ecmp_nexthop_changed != 'no_use'):
        proposed['ecmp_nexthop_changed'] = ecmp_nexthop_changed
    if default_local_pref:
        proposed['default_local_pref'] = default_local_pref
    if default_med:
        proposed['default_med'] = default_med
    if (default_rt_import_enable != 'no_use'):
        proposed['default_rt_import_enable'] = default_rt_import_enable
    if router_id:
        proposed['router_id'] = router_id
    if (vrf_rid_auto_sel != 'no_use'):
        proposed['vrf_rid_auto_sel'] = vrf_rid_auto_sel
    if (nexthop_third_party != 'no_use'):
        proposed['nexthop_third_party'] = nexthop_third_party
    if (summary_automatic != 'no_use'):
        proposed['summary_automatic'] = summary_automatic
    if (auto_frr_enable != 'no_use'):
        proposed['auto_frr_enable'] = auto_frr_enable
    if (load_balancing_as_path_ignore != 'no_use'):
        proposed['load_balancing_as_path_ignore'] = load_balancing_as_path_ignore
    if (rib_only_enable != 'no_use'):
        proposed['rib_only_enable'] = rib_only_enable
    if rib_only_policy_name:
        proposed['rib_only_policy_name'] = rib_only_policy_name
    if (active_route_advertise != 'no_use'):
        proposed['active_route_advertise'] = active_route_advertise
    if (as_path_neglect != 'no_use'):
        proposed['as_path_neglect'] = as_path_neglect
    if (med_none_as_maximum != 'no_use'):
        proposed['med_none_as_maximum'] = med_none_as_maximum
    if (router_id_neglect != 'no_use'):
        proposed['router_id_neglect'] = router_id_neglect
    if (igp_metric_ignore != 'no_use'):
        proposed['igp_metric_ignore'] = igp_metric_ignore
    if (always_compare_med != 'no_use'):
        proposed['always_compare_med'] = always_compare_med
    if (determin_med != 'no_use'):
        proposed['determin_med'] = determin_med
    if preference_external:
        proposed['preference_external'] = preference_external
    if preference_internal:
        proposed['preference_internal'] = preference_internal
    if preference_local:
        proposed['preference_local'] = preference_local
    if prefrence_policy_name:
        proposed['prefrence_policy_name'] = prefrence_policy_name
    if (reflect_between_client != 'no_use'):
        proposed['reflect_between_client'] = reflect_between_client
    if reflector_cluster_id:
        proposed['reflector_cluster_id'] = reflector_cluster_id
    if reflector_cluster_ipv4:
        proposed['reflector_cluster_ipv4'] = reflector_cluster_ipv4
    if rr_filter_number:
        proposed['rr_filter_number'] = rr_filter_number
    if (policy_vpn_target != 'no_use'):
        proposed['policy_vpn_target'] = policy_vpn_target
    if next_hop_sel_depend_type:
        proposed['next_hop_sel_depend_type'] = next_hop_sel_depend_type
    if nhp_relay_route_policy_name:
        proposed['nhp_relay_route_policy_name'] = nhp_relay_route_policy_name
    if (ebgp_if_sensitive != 'no_use'):
        proposed['ebgp_if_sensitive'] = ebgp_if_sensitive
    if (reflect_chg_path != 'no_use'):
        proposed['reflect_chg_path'] = reflect_chg_path
    if add_path_sel_num:
        proposed['add_path_sel_num'] = add_path_sel_num
    if route_sel_delay:
        proposed['route_sel_delay'] = route_sel_delay
    if (allow_invalid_as != 'no_use'):
        proposed['allow_invalid_as'] = allow_invalid_as
    if (policy_ext_comm_enable != 'no_use'):
        proposed['policy_ext_comm_enable'] = policy_ext_comm_enable
    if (supernet_uni_adv != 'no_use'):
        proposed['supernet_uni_adv'] = supernet_uni_adv
    if (supernet_label_adv != 'no_use'):
        proposed['supernet_label_adv'] = supernet_label_adv
    if ingress_lsp_policy_name:
        proposed['ingress_lsp_policy_name'] = ingress_lsp_policy_name
    if (originator_prior != 'no_use'):
        proposed['originator_prior'] = originator_prior
    if (lowest_priority != 'no_use'):
        proposed['lowest_priority'] = lowest_priority
    if (relay_delay_enable != 'no_use'):
        proposed['relay_delay_enable'] = relay_delay_enable
    if import_protocol:
        proposed['import_protocol'] = import_protocol
    if import_process_id:
        proposed['import_process_id'] = import_process_id
    if network_address:
        proposed['network_address'] = network_address
    if mask_len:
        proposed['mask_len'] = mask_len
    bgp_af_rst = ce_bgp_af_obj.check_bgp_af_args(module=module)
    bgp_af_other_rst = ce_bgp_af_obj.check_bgp_af_other_args(module=module)
    bgp_af_other_can_del_rst = ce_bgp_af_obj.check_bgp_af_other_can_del(module=module)
    bgp_import_network_route_rst = ce_bgp_af_obj.check_bgp_import_network_route(module=module)
    exist_tmp = dict()
    for item in bgp_af_rst:
        if (item != 'need_cfg'):
            exist_tmp[item] = bgp_af_rst[item]
    if exist_tmp:
        existing['bgp af'] = exist_tmp
    exist_tmp = dict()
    for item in bgp_af_other_rst:
        if (item != 'need_cfg'):
            exist_tmp[item] = bgp_af_other_rst[item]
    if exist_tmp:
        existing['bgp af other'] = exist_tmp
    exist_tmp = dict()
    for item in bgp_import_network_route_rst:
        if (item != 'need_cfg'):
            exist_tmp[item] = bgp_import_network_route_rst[item]
    if exist_tmp:
        existing['bgp import & network route'] = exist_tmp
    if (state == 'present'):
        if (bgp_af_rst['need_cfg'] and bgp_import_network_route_rst['import_need_cfg'] and bgp_import_network_route_rst['network_need_cfg']):
            changed = True
            if ('af_type' in bgp_af_rst.keys()):
                conf_str = (CE_MERGE_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type))
            else:
                conf_str = (CE_CREATE_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type))
            if ('bgp_import_route' in bgp_import_network_route_rst.keys()):
                conf_str += (CE_BGP_MERGE_IMPORT_UNIT % (import_protocol, import_process_id))
            else:
                conf_str += (CE_BGP_CREATE_IMPORT_UNIT % (import_protocol, import_process_id))
            if ('bgp_network_route' in bgp_import_network_route_rst.keys()):
                conf_str += (CE_BGP_MERGE_NETWORK_UNIT % (network_address, mask_len))
            else:
                conf_str += (CE_BGP_CREATE_NETWORK_UNIT % (network_address, mask_len))
            conf_str += CE_MERGE_BGP_ADDRESS_FAMILY_TAIL
            recv_xml = ce_bgp_af_obj.netconf_set_config(module=module, conf_str=conf_str)
            if ('<ok/>' not in recv_xml):
                module.fail_json(msg='Error: Present bgp af_type import and network route failed.')
            cmd = ('import-route %s %s' % (import_protocol, import_process_id))
            updates.append(cmd)
            cmd = ('network %s %s' % (network_address, mask_len))
            updates.append(cmd)
        elif (bgp_import_network_route_rst['import_need_cfg'] and bgp_import_network_route_rst['network_need_cfg']):
            changed = True
            conf_str = (CE_BGP_IMPORT_NETWORK_ROUTE_HEADER % (vrf_name, af_type))
            if ('bgp_import_route' in bgp_import_network_route_rst.keys()):
                conf_str += (CE_BGP_MERGE_IMPORT_UNIT % (import_protocol, import_process_id))
            else:
                conf_str += (CE_BGP_CREATE_IMPORT_UNIT % (import_protocol, import_process_id))
            if ('bgp_network_route' in bgp_import_network_route_rst.keys()):
                conf_str += (CE_BGP_MERGE_NETWORK_UNIT % (network_address, mask_len))
            else:
                conf_str += (CE_BGP_CREATE_NETWORK_UNIT % (network_address, mask_len))
            conf_str += CE_BGP_IMPORT_NETWORK_ROUTE_TAIL
            recv_xml = ce_bgp_af_obj.netconf_set_config(module=module, conf_str=conf_str)
            if ('<ok/>' not in recv_xml):
                module.fail_json(msg='Error: Present bgp import and network route failed.')
            cmd = ('import-route %s %s' % (import_protocol, import_process_id))
            updates.append(cmd)
            cmd = ('network %s %s' % (network_address, mask_len))
            updates.append(cmd)
        else:
            if bgp_af_rst['need_cfg']:
                if ('af_type' in bgp_af_rst.keys()):
                    cmd = ce_bgp_af_obj.merge_bgp_af(module=module)
                    changed = True
                    for item in cmd:
                        updates.append(item)
                else:
                    cmd = ce_bgp_af_obj.create_bgp_af(module=module)
                    changed = True
                    for item in cmd:
                        updates.append(item)
            if bgp_af_other_rst['need_cfg']:
                cmd = ce_bgp_af_obj.merge_bgp_af_other(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
            if bgp_import_network_route_rst['import_need_cfg']:
                if ('bgp_import_route' in bgp_import_network_route_rst.keys()):
                    cmd = ce_bgp_af_obj.merge_bgp_import_route(module=module)
                    changed = True
                    for item in cmd:
                        updates.append(item)
                else:
                    cmd = ce_bgp_af_obj.create_bgp_import_route(module=module)
                    changed = True
                    for item in cmd:
                        updates.append(item)
            if bgp_import_network_route_rst['network_need_cfg']:
                if ('bgp_network_route' in bgp_import_network_route_rst.keys()):
                    cmd = ce_bgp_af_obj.merge_bgp_network_route(module=module)
                    changed = True
                    for item in cmd:
                        updates.append(item)
                else:
                    cmd = ce_bgp_af_obj.create_bgp_network_route(module=module)
                    changed = True
                    for item in cmd:
                        updates.append(item)
    else:
        if (bgp_import_network_route_rst['import_need_cfg'] and bgp_import_network_route_rst['network_need_cfg']):
            changed = True
            conf_str = (CE_BGP_IMPORT_NETWORK_ROUTE_HEADER % (vrf_name, af_type))
            conf_str += (CE_BGP_DELETE_IMPORT_UNIT % (import_protocol, import_process_id))
            conf_str += (CE_BGP_DELETE_NETWORK_UNIT % (network_address, mask_len))
            conf_str += CE_BGP_IMPORT_NETWORK_ROUTE_TAIL
            recv_xml = ce_bgp_af_obj.netconf_set_config(module=module, conf_str=conf_str)
            if ('<ok/>' not in recv_xml):
                module.fail_json(msg='Error: Absent bgp import and network route failed.')
            cmd = ('undo import-route %s %s' % (import_protocol, import_process_id))
            updates.append(cmd)
            cmd = ('undo network %s %s' % (network_address, mask_len))
            updates.append(cmd)
        else:
            if bgp_import_network_route_rst['import_need_cfg']:
                cmd = ce_bgp_af_obj.delete_bgp_import_route(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
            if bgp_import_network_route_rst['network_need_cfg']:
                cmd = ce_bgp_af_obj.delete_bgp_network_route(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
        if bgp_af_other_can_del_rst['need_cfg']:
            cmd = ce_bgp_af_obj.delete_bgp_af_other(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        if (bgp_af_rst['need_cfg'] and (not bgp_af_other_can_del_rst['need_cfg'])):
            cmd = ce_bgp_af_obj.delete_bgp_af(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        if bgp_af_other_rst['need_cfg']:
            pass
    bgp_af_rst = ce_bgp_af_obj.check_bgp_af_args(module=module)
    end_tmp = dict()
    for item in bgp_af_rst:
        if (item != 'need_cfg'):
            end_tmp[item] = bgp_af_rst[item]
    if end_tmp:
        end_state['bgp af'] = end_tmp
    bgp_af_other_rst = ce_bgp_af_obj.check_bgp_af_other_args(module=module)
    end_tmp = dict()
    for item in bgp_af_other_rst:
        if (item != 'need_cfg'):
            end_tmp[item] = bgp_af_other_rst[item]
    if end_tmp:
        end_state['bgp af other'] = end_tmp
    bgp_import_network_route_rst = ce_bgp_af_obj.check_bgp_import_network_route(module=module)
    end_tmp = dict()
    for item in bgp_import_network_route_rst:
        if (item != 'need_cfg'):
            end_tmp[item] = bgp_import_network_route_rst[item]
    if end_tmp:
        end_state['bgp import & network route'] = end_tmp
    results = dict()
    results['proposed'] = proposed
    results['existing'] = existing
    results['changed'] = changed
    results['end_state'] = end_state
    results['updates'] = updates
    module.exit_json(**results)