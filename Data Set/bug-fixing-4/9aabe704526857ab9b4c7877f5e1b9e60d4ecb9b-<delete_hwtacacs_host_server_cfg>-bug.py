def delete_hwtacacs_host_server_cfg(self, **kwargs):
    ' Delete hwtacacs host server configure '
    module = kwargs['module']
    hwtacacs_template = module.params['hwtacacs_template']
    hwtacacs_server_host_name = module.params['hwtacacs_server_host_name']
    hwtacacs_server_type = module.params['hwtacacs_server_type']
    hwtacacs_is_secondary_server = module.params['hwtacacs_is_secondary_server']
    hwtacacs_vpn_name = module.params['hwtacacs_vpn_name']
    hwtacacs_is_public_net = module.params['hwtacacs_is_public_net']
    conf_str = (CE_DELETE_HWTACACS_HOST_SERVER_CFG % (hwtacacs_template, hwtacacs_server_host_name, hwtacacs_server_type, str(hwtacacs_is_secondary_server).lower(), hwtacacs_vpn_name, str(hwtacacs_is_public_net).lower()))
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Delete hwtacacs host server config failed.')
    cmds = []
    if (hwtacacs_server_type == 'Authentication'):
        cmd = ('undo hwtacacs server authentication host host-name %s' % hwtacacs_server_host_name)
        if (hwtacacs_vpn_name and (hwtacacs_vpn_name != '_public_')):
            cmd += (' vpn-instance %s' % hwtacacs_vpn_name)
        if hwtacacs_is_public_net:
            cmd += ' public-net'
        if hwtacacs_is_secondary_server:
            cmd += ' secondary'
    elif (hwtacacs_server_type == 'Authorization'):
        cmd = ('undo hwtacacs server authorization host host-name %s' % hwtacacs_server_host_name)
        if (hwtacacs_vpn_name and (hwtacacs_vpn_name != '_public_')):
            cmd += (' vpn-instance %s' % hwtacacs_vpn_name)
        if hwtacacs_is_public_net:
            cmd += ' public-net'
        if hwtacacs_is_secondary_server:
            cmd += ' secondary'
    elif (hwtacacs_server_type == 'Accounting'):
        cmd = ('undo hwtacacs server accounting host host-name %s' % hwtacacs_server_host_name)
        if (hwtacacs_vpn_name and (hwtacacs_vpn_name != '_public_')):
            cmd += (' vpn-instance %s' % hwtacacs_vpn_name)
        if hwtacacs_is_public_net:
            cmd += ' public-net'
        if hwtacacs_is_secondary_server:
            cmd += ' secondary'
    elif (hwtacacs_server_type == 'Common'):
        cmd = ('undo hwtacacs server host host-name %s' % hwtacacs_server_host_name)
        if (hwtacacs_vpn_name and (hwtacacs_vpn_name != '_public_')):
            cmd += (' vpn-instance %s' % hwtacacs_vpn_name)
        if hwtacacs_is_public_net:
            cmd += ' public-net'
        if hwtacacs_is_secondary_server:
            cmd += ' secondary'
    cmds.append(cmd)
    return cmds