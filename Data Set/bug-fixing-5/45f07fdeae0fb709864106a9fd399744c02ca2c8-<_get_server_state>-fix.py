def _get_server_state(module, cloud):
    state = module.params['state']
    server = cloud.get_server(module.params['name'])
    if (server and (state == 'present')):
        if (server.status not in ('ACTIVE', 'SHUTOFF', 'PAUSED', 'SUSPENDED')):
            module.fail_json(msg=('The instance is available but not Active state: ' + server.status))
        (ip_changed, server) = _check_ips(module, cloud, server)
        (sg_changed, server) = _check_security_groups(module, cloud, server)
        (server_changed, server) = _update_server(module, cloud, server)
        _exit_hostvars(module, cloud, server, (ip_changed or sg_changed or server_changed))
    if (server and (state == 'absent')):
        return True
    if (state == 'absent'):
        module.exit_json(changed=False, result='not present')
    return True