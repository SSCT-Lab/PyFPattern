def target_login(module, target):
    node_auth = module.params['node_auth']
    node_user = module.params['node_user']
    node_pass = module.params['node_pass']
    if node_user:
        params = [('node.session.auth.authmethod', node_auth), ('node.session.auth.username', node_user), ('node.session.auth.password', node_pass)]
        for (name, value) in params:
            cmd = ('%s --mode node --targetname %s --op=update --name %s --value %s' % (iscsiadm_cmd, target, name, value))
            (rc, out, err) = module.run_command(cmd)
            if (rc > 0):
                module.fail_json(cmd=cmd, rc=rc, msg=err)
    cmd = ('%s --mode node --targetname %s --login' % (iscsiadm_cmd, target))
    (rc, out, err) = module.run_command(cmd)
    if (rc > 0):
        module.fail_json(cmd=cmd, rc=rc, msg=err)