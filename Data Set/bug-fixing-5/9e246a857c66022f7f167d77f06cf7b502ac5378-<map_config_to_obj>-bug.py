def map_config_to_obj(module):
    templatized_command = '%(ovs-vsctl)s -t %(timeout)s list-br'
    command = (templatized_command % module.params)
    (rc, out, err) = module.run_command(command, check_rc=True)
    if (rc != 0):
        module.fail_json(msg=err)
    obj = {
        
    }
    if (module.params['bridge'] in out.splitlines()):
        obj['bridge'] = module.params['bridge']
        templatized_command = '%(ovs-vsctl)s -t %(timeout)s br-to-parent %(bridge)s'
        command = (templatized_command % module.params)
        (rc, out, err) = module.run_command(command, check_rc=True)
        obj['parent'] = out.strip()
        templatized_command = '%(ovs-vsctl)s -t %(timeout)s br-to-vlan %(bridge)s'
        command = (templatized_command % module.params)
        (rc, out, err) = module.run_command(command, check_rc=True)
        obj['vlan'] = out.strip()
        templatized_command = '%(ovs-vsctl)s -t %(timeout)s get-fail-mode %(bridge)s'
        command = (templatized_command % module.params)
        (rc, out, err) = module.run_command(command, check_rc=True)
        obj['fail_mode'] = out.strip()
        templatized_command = '%(ovs-vsctl)s -t %(timeout)s br-get-external-id %(bridge)s'
        command = (templatized_command % module.params)
        (rc, out, err) = module.run_command(command, check_rc=True)
        obj['external_ids'] = _external_ids_to_dict(out)
    return obj