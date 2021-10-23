def delete_bgp_af(self, **kwargs):
    ' delete_bgp_af '
    module = kwargs['module']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    conf_str = ((CE_DELETE_BGP_ADDRESS_FAMILY_HEADER % (vrf_name, af_type)) + CE_DELETE_BGP_ADDRESS_FAMILY_TAIL)
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Delete bgp address family failed.')
    cmds = []
    cmd = ('undo ipv4-family vpn-instance %s' % vrf_name)
    cmds.append(cmd)
    if (af_type == 'ipv4multi'):
        cmd = 'undo ipv4-family multicast'
    elif (af_type == 'ipv4vpn'):
        cmd = 'undo ipv4-family vpnv4'
    elif (af_type == 'ipv6uni'):
        cmd = 'undo ipv6-family unicast'
    elif (af_type == 'ipv6vpn'):
        cmd = 'undo ipv6-family vpnv6'
    elif (af_type == 'evpn'):
        cmd = ('undo ipv6-family vpn-instance %s' % vrf_name)
    cmds.append(cmd)
    return cmds