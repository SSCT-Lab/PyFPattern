def merge_bgp_instance_other(self, **kwargs):
    ' merge_bgp_instance_other '
    module = kwargs['module']
    conf_str = CE_MERGE_BGP_INSTANCE_HEADER
    vrf_name = module.params['vrf_name']
    conf_str += ('<vrfName>%s</vrfName>' % vrf_name)
    cmds = []
    default_af_type = module.params['default_af_type']
    if default_af_type:
        conf_str += ('<defaultAfType>%s</defaultAfType>' % default_af_type)
        if (vrf_name != '_public_'):
            if (default_af_type == 'ipv6uni'):
                cmd = ('ipv6-family vpn-instance %s' % vrf_name)
                cmds.append(cmd)
    vrf_rid_auto_sel = module.params['vrf_rid_auto_sel']
    if (vrf_rid_auto_sel != 'no_use'):
        conf_str += ('<vrfRidAutoSel>%s</vrfRidAutoSel>' % vrf_rid_auto_sel)
        if (vrf_rid_auto_sel == 'true'):
            cmd = 'router-id auto-select'
        else:
            cmd = 'undo router-id auto-select'
        cmds.append(cmd)
    router_id = module.params['router_id']
    if router_id:
        conf_str += ('<routerId>%s</routerId>' % router_id)
        cmd = ('router-id %s' % router_id)
        cmds.append(cmd)
    keepalive_time = module.params['keepalive_time']
    if keepalive_time:
        conf_str += ('<keepaliveTime>%s</keepaliveTime>' % keepalive_time)
        cmd = ('timer keepalive %s' % keepalive_time)
        cmds.append(cmd)
    hold_time = module.params['hold_time']
    if hold_time:
        conf_str += ('<holdTime>%s</holdTime>' % hold_time)
        cmd = ('timer hold %s' % hold_time)
        cmds.append(cmd)
    min_hold_time = module.params['min_hold_time']
    if min_hold_time:
        conf_str += ('<minHoldTime>%s</minHoldTime>' % min_hold_time)
        cmd = ('timer min-holdtime %s' % min_hold_time)
        cmds.append(cmd)
    conn_retry_time = module.params['conn_retry_time']
    if conn_retry_time:
        conf_str += ('<connRetryTime>%s</connRetryTime>' % conn_retry_time)
        cmd = ('timer connect-retry %s' % conn_retry_time)
        cmds.append(cmd)
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    if (ebgp_if_sensitive != 'no_use'):
        conf_str += ('<ebgpIfSensitive>%s</ebgpIfSensitive>' % ebgp_if_sensitive)
        if (ebgp_if_sensitive == 'true'):
            cmd = 'ebgp-interface-sensitive'
        else:
            cmd = 'undo ebgp-interface-sensitive'
        cmds.append(cmd)
    conf_str += CE_MERGE_BGP_INSTANCE_TAIL
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Merge bgp instance other failed.')
    return cmds