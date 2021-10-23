def main():
    ' main '
    argument_spec = dict(state=dict(choices=['present', 'absent'], default='present'), as_number=dict(type='str'), graceful_restart=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), time_wait_for_rib=dict(type='str'), as_path_limit=dict(type='str'), check_first_as=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), confed_id_number=dict(type='str'), confed_nonstanded=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), bgp_rid_auto_sel=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), keep_all_routes=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), memory_limit=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), gr_peer_reset=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), is_shutdown=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), suppress_interval=dict(type='str'), hold_interval=dict(type='str'), clear_interval=dict(type='str'), confed_peer_as_num=dict(type='str'), vrf_name=dict(type='str'), vrf_rid_auto_sel=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), router_id=dict(type='str'), keepalive_time=dict(type='str'), hold_time=dict(type='str'), min_hold_time=dict(type='str'), conn_retry_time=dict(type='str'), ebgp_if_sensitive=dict(type='str', default='no_use', choices=['no_use', 'true', 'false']), default_af_type=dict(type='str', choices=['ipv4uni', 'ipv6uni']))
    argument_spec.update(ce_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    changed = False
    proposed = dict()
    existing = dict()
    end_state = dict()
    updates = []
    state = module.params['state']
    as_number = module.params['as_number']
    graceful_restart = module.params['graceful_restart']
    time_wait_for_rib = module.params['time_wait_for_rib']
    as_path_limit = module.params['as_path_limit']
    check_first_as = module.params['check_first_as']
    confed_id_number = module.params['confed_id_number']
    confed_nonstanded = module.params['confed_nonstanded']
    bgp_rid_auto_sel = module.params['bgp_rid_auto_sel']
    keep_all_routes = module.params['keep_all_routes']
    memory_limit = module.params['memory_limit']
    gr_peer_reset = module.params['gr_peer_reset']
    is_shutdown = module.params['is_shutdown']
    suppress_interval = module.params['suppress_interval']
    hold_interval = module.params['hold_interval']
    clear_interval = module.params['clear_interval']
    confed_peer_as_num = module.params['confed_peer_as_num']
    router_id = module.params['router_id']
    vrf_name = module.params['vrf_name']
    vrf_rid_auto_sel = module.params['vrf_rid_auto_sel']
    keepalive_time = module.params['keepalive_time']
    hold_time = module.params['hold_time']
    min_hold_time = module.params['min_hold_time']
    conn_retry_time = module.params['conn_retry_time']
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    default_af_type = module.params['default_af_type']
    ce_bgp_obj = Bgp()
    if (not ce_bgp_obj):
        module.fail_json(msg='Error: Init module failed.')
    proposed['state'] = state
    if as_number:
        proposed['as_number'] = as_number
    if (graceful_restart != 'no_use'):
        proposed['graceful_restart'] = graceful_restart
    if time_wait_for_rib:
        proposed['time_wait_for_rib'] = time_wait_for_rib
    if as_path_limit:
        proposed['as_path_limit'] = as_path_limit
    if (check_first_as != 'no_use'):
        proposed['check_first_as'] = check_first_as
    if confed_id_number:
        proposed['confed_id_number'] = confed_id_number
    if (confed_nonstanded != 'no_use'):
        proposed['confed_nonstanded'] = confed_nonstanded
    if (bgp_rid_auto_sel != 'no_use'):
        proposed['bgp_rid_auto_sel'] = bgp_rid_auto_sel
    if (keep_all_routes != 'no_use'):
        proposed['keep_all_routes'] = keep_all_routes
    if (memory_limit != 'no_use'):
        proposed['memory_limit'] = memory_limit
    if (gr_peer_reset != 'no_use'):
        proposed['gr_peer_reset'] = gr_peer_reset
    if (is_shutdown != 'no_use'):
        proposed['is_shutdown'] = is_shutdown
    if suppress_interval:
        proposed['suppress_interval'] = suppress_interval
    if hold_interval:
        proposed['hold_interval'] = hold_interval
    if clear_interval:
        proposed['clear_interval'] = clear_interval
    if confed_peer_as_num:
        proposed['confed_peer_as_num'] = confed_peer_as_num
    if router_id:
        proposed['router_id'] = router_id
    if vrf_name:
        proposed['vrf_name'] = vrf_name
    if (vrf_rid_auto_sel != 'no_use'):
        proposed['vrf_rid_auto_sel'] = vrf_rid_auto_sel
    if keepalive_time:
        proposed['keepalive_time'] = keepalive_time
    if hold_time:
        proposed['hold_time'] = hold_time
    if min_hold_time:
        proposed['min_hold_time'] = min_hold_time
    if conn_retry_time:
        proposed['conn_retry_time'] = conn_retry_time
    if (ebgp_if_sensitive != 'no_use'):
        proposed['ebgp_if_sensitive'] = ebgp_if_sensitive
    if default_af_type:
        proposed['default_af_type'] = default_af_type
    need_bgp_enable = check_bgp_enable_args(module=module)
    need_bgp_enable_other_rst = ce_bgp_obj.check_bgp_enable_other_args(module=module)
    need_bgp_confed = check_bgp_confed_args(module=module)
    need_bgp_instance = ce_bgp_obj.check_bgp_instance_args(module=module)
    need_bgp_instance_other_rst = ce_bgp_obj.check_bgp_instance_other_args(module=module)
    if need_bgp_enable:
        bgp_enable_exist = ce_bgp_obj.get_bgp_enable(module=module)
        existing['bgp enable'] = bgp_enable_exist
        if bgp_enable_exist:
            asnumber_exist = bgp_enable_exist[0][0]
            bgpenable_exist = bgp_enable_exist[0][1]
        else:
            asnumber_exist = None
            bgpenable_exist = None
        if (state == 'present'):
            bgp_enable_new = (as_number, 'true')
            if (bgp_enable_new in bgp_enable_exist):
                pass
            elif ((bgpenable_exist == 'true') and (asnumber_exist != as_number)):
                module.fail_json(msg=('Error: BGP is already running. The AS is %s.' % asnumber_exist))
            else:
                cmd = ce_bgp_obj.merge_bgp_enable(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
        elif (need_bgp_enable_other_rst['need_cfg'] or need_bgp_confed or need_bgp_instance_other_rst['need_cfg']):
            pass
        elif (bgpenable_exist == 'false'):
            pass
        elif ((bgpenable_exist == 'true') and (asnumber_exist == as_number)):
            cmd = ce_bgp_obj.merge_bgp_enable(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        else:
            module.fail_json(msg=('Error: BGP is already running. The AS is %s.' % asnumber_exist))
        bgp_enable_end = ce_bgp_obj.get_bgp_enable(module=module)
        end_state['bgp enable'] = bgp_enable_end
    exist_tmp = dict()
    for item in need_bgp_enable_other_rst:
        if (item != 'need_cfg'):
            exist_tmp[item] = need_bgp_enable_other_rst[item]
    if exist_tmp:
        existing['bgp enable other'] = exist_tmp
    if need_bgp_enable_other_rst['need_cfg']:
        if (state == 'present'):
            cmd = ce_bgp_obj.merge_bgp_enable_other(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        else:
            cmd = ce_bgp_obj.delete_bgp_enable_other(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
    need_bgp_enable_other_rst = ce_bgp_obj.check_bgp_enable_other_args(module=module)
    end_tmp = dict()
    for item in need_bgp_enable_other_rst:
        if (item != 'need_cfg'):
            end_tmp[item] = need_bgp_enable_other_rst[item]
    if end_tmp:
        end_state['bgp enable other'] = end_tmp
    if need_bgp_confed:
        confed_exist = ce_bgp_obj.get_bgp_confed_peer_as(module=module)
        existing['confederation peer as'] = confed_exist
        confed_new = confed_peer_as_num
        if (state == 'present'):
            if (len(confed_exist) == 0):
                cmd = ce_bgp_obj.create_bgp_confed_peer_as(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
            elif (confed_new not in confed_exist):
                cmd = ce_bgp_obj.merge_bgp_confed_peer_as(module=module)
                changed = True
                for item in cmd:
                    updates.append(item)
        elif (len(confed_exist) == 0):
            pass
        elif (confed_new not in confed_exist):
            pass
        else:
            cmd = ce_bgp_obj.delete_bgp_confed_peer_as(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        confed_end = ce_bgp_obj.get_bgp_confed_peer_as(module=module)
        end_state['confederation peer as'] = confed_end
    router_id_exist = ce_bgp_obj.get_bgp_instance(module=module)
    existing['bgp instance'] = router_id_exist
    if need_bgp_instance:
        router_id_new = vrf_name
        if (state == 'present'):
            if (len(router_id_exist) == 0):
                cmd = ce_bgp_obj.create_bgp_instance(module=module)
                changed = True
                updates.append(cmd)
            elif (router_id_new not in router_id_exist):
                ce_bgp_obj.merge_bgp_instance(module=module)
                changed = True
        elif (not need_bgp_instance_other_rst['need_cfg']):
            if (vrf_name != '_public_'):
                if (len(router_id_exist) == 0):
                    pass
                elif (router_id_new not in router_id_exist):
                    pass
                else:
                    cmd = ce_bgp_obj.delete_bgp_instance(module=module)
                    changed = True
                    for item in cmd:
                        updates.append(item)
    router_id_end = ce_bgp_obj.get_bgp_instance(module=module)
    end_state['bgp instance'] = router_id_end
    exist_tmp = dict()
    for item in need_bgp_instance_other_rst:
        if (item != 'need_cfg'):
            exist_tmp[item] = need_bgp_instance_other_rst[item]
    if exist_tmp:
        existing['bgp instance other'] = exist_tmp
    if need_bgp_instance_other_rst['need_cfg']:
        if (state == 'present'):
            cmd = ce_bgp_obj.merge_bgp_instance_other(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        elif (vrf_name == '_public_'):
            cmd = ce_bgp_obj.delete_instance_other_public(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
        else:
            cmd = ce_bgp_obj.delete_bgp_instance_other_comm(module=module)
            changed = True
            for item in cmd:
                updates.append(item)
    need_bgp_instance_other_rst = ce_bgp_obj.check_bgp_instance_other_args(module=module)
    end_tmp = dict()
    for item in need_bgp_instance_other_rst:
        if (item != 'need_cfg'):
            end_tmp[item] = need_bgp_instance_other_rst[item]
    if end_tmp:
        end_state['bgp instance other'] = end_tmp
    if (end_state == existing):
        changed = False
        updates = list()
    results = dict()
    results['proposed'] = proposed
    results['existing'] = existing
    results['changed'] = changed
    results['end_state'] = end_state
    results['updates'] = updates
    module.exit_json(**results)