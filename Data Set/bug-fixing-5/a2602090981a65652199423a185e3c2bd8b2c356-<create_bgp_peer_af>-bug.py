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
        cmd = 'ipv4-family unicast'
    elif (af_type == 'ipv4multi'):
        cmd = 'ipv4-family multicast'
    elif (af_type == 'ipv6uni'):
        cmd = 'ipv6-family unicast'
    cmds.append(cmd)
    cmd = ('peer %s' % remote_address)
    cmds.append(cmd)
    return cmds