def create_bgp_peer_af(self, **kwargs):
    ' create_bgp_peer_af '
    module = kwargs['module']
    vrf_name = module.params['vrf_name']
    af_type = module.params['af_type']
    remote_address = module.params['remote_address']
    conf_str = (CE_CREATE_BGP_PEER_AF % (vrf_name, af_type, remote_address))
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Create bgp peer address family failed.')
    cmds = []
    cmd = af_type
    if (af_type == 'ipv4uni'):
        if (vrf_name == '_public_'):
            cmd = 'ipv4-family unicast'
        else:
            cmd = ('ipv4-family vpn-instance %s' % vrf_name)
    elif (af_type == 'ipv4multi'):
        cmd = 'ipv4-family multicast'
    elif (af_type == 'ipv6uni'):
        if (vrf_name == '_public_'):
            cmd = 'ipv6-family unicast'
        else:
            cmd = ('ipv6-family vpn-instance %s' % vrf_name)
    elif (af_type == 'evpn'):
        cmd = 'l2vpn-family evpn'
    elif (af_type == 'ipv4vpn'):
        cmd = 'ipv4-family vpnv4'
    elif (af_type == 'ipv6vpn'):
        cmd = 'ipv6-family vpnv6'
    cmds.append(cmd)
    if (vrf_name == '_public_'):
        cmd = ('peer %s enable' % remote_address)
    else:
        cmd = ('peer %s' % remote_address)
    cmds.append(cmd)
    return cmds