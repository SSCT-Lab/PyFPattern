def delete_instance_other_public(self, **kwargs):
    ' delete_instance_other_public '
    module = kwargs['module']
    conf_str = CE_MERGE_BGP_INSTANCE_HEADER
    vrf_name = module.params['vrf_name']
    conf_str += ('<vrfName>%s</vrfName>' % vrf_name)
    cmds = []
    router_id = module.params['router_id']
    if router_id:
        conf_str += '<routerId></routerId>'
        cmd = 'undo router-id'
        cmds.append(cmd)
    vrf_rid_auto_sel = module.params['vrf_rid_auto_sel']
    if (vrf_rid_auto_sel != 'no_use'):
        conf_str += ('<vrfRidAutoSel>%s</vrfRidAutoSel>' % vrf_rid_auto_sel)
        cmd = 'undo router-id vpn-instance auto-select'
        cmds.append(cmd)
    keepalive_time = module.params['keepalive_time']
    if keepalive_time:
        conf_str += ('<keepaliveTime>%s</keepaliveTime>' % '60')
        cmd = 'undo timer keepalive'
        cmds.append(cmd)
    hold_time = module.params['hold_time']
    if hold_time:
        conf_str += ('<holdTime>%s</holdTime>' % '180')
        cmd = 'undo timer hold'
        cmds.append(cmd)
    min_hold_time = module.params['min_hold_time']
    if min_hold_time:
        conf_str += ('<minHoldTime>%s</minHoldTime>' % '0')
        cmd = 'undo timer min-holdtime'
        cmds.append(cmd)
    conn_retry_time = module.params['conn_retry_time']
    if conn_retry_time:
        conf_str += ('<connRetryTime>%s</connRetryTime>' % '32')
        cmd = 'undo timer connect-retry'
        cmds.append(cmd)
    ebgp_if_sensitive = module.params['ebgp_if_sensitive']
    if (ebgp_if_sensitive != 'no_use'):
        conf_str += ('<ebgpIfSensitive>%s</ebgpIfSensitive>' % 'true')
        cmd = 'undo ebgp-interface-sensitive'
        cmds.append(cmd)
    default_af_type = module.params['default_af_type']
    if default_af_type:
        conf_str += ('<defaultAfType>%s</defaultAfType>' % 'ipv4uni')
        if (vrf_name != '_public_'):
            if (default_af_type == 'ipv6uni'):
                cmd = ('undo ipv6-family vpn-instance %s' % vrf_name)
                cmds.append(cmd)
            else:
                cmd = ('undo ipv4-family vpn-instance %s' % vrf_name)
                cmds.append(cmd)
    elif (vrf_name != '_public_'):
        cmd = ('undo ipv4-family vpn-instance %s' % vrf_name)
        cmds.append(cmd)
    conf_str += CE_MERGE_BGP_INSTANCE_TAIL
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Delete default vpn bgp instance other args failed.')
    return cmds