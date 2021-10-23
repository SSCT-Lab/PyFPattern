def main():
    module = AnsibleModule(argument_spec=dict(portal=dict(required=False, aliases=['ip']), port=dict(required=False, default=3260), target=dict(required=False, aliases=['name', 'targetname']), node_auth=dict(required=False, default='CHAP'), node_user=dict(required=False), node_pass=dict(required=False, no_log=True), login=dict(type='bool', aliases=['state']), auto_node_startup=dict(type='bool', aliases=['automatic']), discover=dict(type='bool', default=False), show_nodes=dict(type='bool', default=False)), required_together=[['discover_user', 'discover_pass'], ['node_user', 'node_pass']], supports_check_mode=True)
    global iscsiadm_cmd
    iscsiadm_cmd = module.get_bin_path('iscsiadm', required=True)
    portal = module.params['portal']
    target = module.params['target']
    port = module.params['port']
    login = module.params['login']
    automatic = module.params['auto_node_startup']
    discover = module.params['discover']
    show_nodes = module.params['show_nodes']
    check = module.check_mode
    cached = iscsi_get_cached_nodes(module, portal)
    result = {
        
    }
    result['changed'] = False
    if discover:
        if (portal is None):
            module.fail_json(msg='Need to specify at least the portal (ip) to discover')
        elif check:
            nodes = cached
        else:
            iscsi_discover(module, portal, port)
            nodes = iscsi_get_cached_nodes(module, portal)
        if (not compare_nodelists(cached, nodes)):
            result['changed'] |= True
            result['cache_updated'] = True
    else:
        nodes = cached
    if ((login is not None) or (automatic is not None)):
        if (target is None):
            if (len(nodes) > 1):
                module.fail_json(msg='Need to specify a target')
            else:
                target = nodes[0]
        else:
            check_target = False
            for node in nodes:
                if (node == target):
                    check_target = True
                    break
            if (not check_target):
                module.fail_json(msg='Specified target not found')
    if show_nodes:
        result['nodes'] = nodes
    if (login is not None):
        loggedon = target_loggedon(module, target)
        if ((login and loggedon) or ((not login) and (not loggedon))):
            result['changed'] |= False
            if login:
                result['devicenodes'] = target_device_node(module, target)
        elif (not check):
            if login:
                target_login(module, target)
                time.sleep(1)
                result['devicenodes'] = target_device_node(module, target)
            else:
                target_logout(module, target)
            result['changed'] |= True
            result['connection_changed'] = True
        else:
            result['changed'] |= True
            result['connection_changed'] = True
    if (automatic is not None):
        isauto = target_isauto(module, target)
        if ((automatic and isauto) or ((not automatic) and (not isauto))):
            result['changed'] |= False
            result['automatic_changed'] = False
        elif (not check):
            if automatic:
                target_setauto(module, target)
            else:
                target_setmanual(module, target)
            result['changed'] |= True
            result['automatic_changed'] = True
        else:
            result['changed'] |= True
            result['automatic_changed'] = True
    module.exit_json(**result)