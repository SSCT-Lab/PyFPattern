def delete_bgp_enable_other(self, **kwargs):
    ' delete bgp enable other args '
    module = kwargs['module']
    conf_str = CE_MERGE_BGP_ENABLE_HEADER
    cmds = []
    graceful_restart = module.params['graceful_restart']
    if (graceful_restart != 'no_use'):
        conf_str += ('<gracefulRestart>%s</gracefulRestart>' % graceful_restart)
        if (graceful_restart == 'true'):
            cmd = 'graceful-restart'
        else:
            cmd = 'undo graceful-restart'
        cmds.append(cmd)
    time_wait_for_rib = module.params['time_wait_for_rib']
    if time_wait_for_rib:
        conf_str += '<timeWaitForRib>600</timeWaitForRib>'
        cmd = 'undo graceful-restart timer wait-for-rib'
        cmds.append(cmd)
    as_path_limit = module.params['as_path_limit']
    if as_path_limit:
        conf_str += '<asPathLimit>255</asPathLimit>'
        cmd = 'undo as-path-limit'
        cmds.append(cmd)
    check_first_as = module.params['check_first_as']
    if (check_first_as != 'no_use'):
        conf_str += ('<checkFirstAs>%s</checkFirstAs>' % check_first_as)
        if (check_first_as == 'true'):
            cmd = 'check-first-as'
        else:
            cmd = 'undo check-first-as'
        cmds.append(cmd)
    confed_id_number = module.params['confed_id_number']
    if confed_id_number:
        conf_str += '<confedIdNumber></confedIdNumber>'
        cmd = 'undo confederation id'
        cmds.append(cmd)
    confed_nonstanded = module.params['confed_nonstanded']
    if (confed_nonstanded != 'no_use'):
        conf_str += ('<confedNonstanded>%s</confedNonstanded>' % confed_nonstanded)
        if (confed_nonstanded == 'true'):
            cmd = 'confederation nonstandard'
        else:
            cmd = 'undo confederation nonstandard'
        cmds.append(cmd)
    bgp_rid_auto_sel = module.params['bgp_rid_auto_sel']
    if (bgp_rid_auto_sel != 'no_use'):
        conf_str += ('<bgpRidAutoSel>%s</bgpRidAutoSel>' % bgp_rid_auto_sel)
        if (bgp_rid_auto_sel == 'true'):
            cmd = 'router-id vpn-instance auto-select'
        else:
            cmd = 'undo router-id'
        cmds.append(cmd)
    keep_all_routes = module.params['keep_all_routes']
    if (keep_all_routes != 'no_use'):
        conf_str += ('<keepAllRoutes>%s</keepAllRoutes>' % keep_all_routes)
        if (keep_all_routes == 'true'):
            cmd = 'keep-all-routes'
        else:
            cmd = 'undo keep-all-routes'
        cmds.append(cmd)
    memory_limit = module.params['memory_limit']
    if (memory_limit != 'no_use'):
        conf_str += ('<memoryLimit>%s</memoryLimit>' % memory_limit)
        if (memory_limit == 'true'):
            cmd = 'prefix memory-limit'
        else:
            cmd = 'undo prefix memory-limit'
        cmds.append(cmd)
    gr_peer_reset = module.params['gr_peer_reset']
    if (gr_peer_reset != 'no_use'):
        conf_str += ('<grPeerReset>%s</grPeerReset>' % gr_peer_reset)
        if (gr_peer_reset == 'true'):
            cmd = 'graceful-restart peer-reset'
        else:
            cmd = 'undo graceful-restart peer-reset'
        cmds.append(cmd)
    is_shutdown = module.params['is_shutdown']
    if (is_shutdown != 'no_use'):
        conf_str += ('<isShutdown>%s</isShutdown>' % is_shutdown)
        if (is_shutdown == 'true'):
            cmd = 'shutdown'
        else:
            cmd = 'undo shutdown'
        cmds.append(cmd)
    suppress_interval = module.params['suppress_interval']
    hold_interval = module.params['hold_interval']
    clear_interval = module.params['clear_interval']
    if suppress_interval:
        conf_str += '<suppressInterval>60</suppressInterval>'
        cmd = ('nexthop recursive-lookup restrain suppress-interval %s hold-interval %s clear-interval %s' % (suppress_interval, hold_interval, clear_interval))
        cmds.append(cmd)
    if hold_interval:
        conf_str += '<holdInterval>120</holdInterval>'
    if clear_interval:
        conf_str += '<clearInterval>600</clearInterval>'
    conf_str += CE_MERGE_BGP_ENABLE_TAIL
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Delete bgp enable failed.')
    return cmds