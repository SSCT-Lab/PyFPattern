def main():
    module = AnsibleModule(argument_spec=dict(state=dict(type='str', choices=['enabled', 'disabled', 'reloaded', 'reset']), default=dict(type='str', aliases=['policy'], choices=['allow', 'deny', 'reject']), logging=dict(type='str', choices=['full', 'high', 'low', 'medium', 'off', 'on']), direction=dict(type='str', choices=['in', 'incoming', 'out', 'outgoing', 'routed']), delete=dict(type='bool', default=False), route=dict(type='bool', default=False), insert=dict(type='str'), rule=dict(type='str', choices=['allow', 'deny', 'limit', 'reject']), interface=dict(type='str', aliases=['if']), log=dict(type='bool', default=False), from_ip=dict(type='str', default='any', aliases=['from', 'src']), from_port=dict(type='str'), to_ip=dict(type='str', default='any', aliases=['dest', 'to']), to_port=dict(type='str', aliases=['port']), proto=dict(type='str', aliases=['protocol'], choices=['ah', 'any', 'esp', 'ipv6', 'tcp', 'udp']), app=dict(type='str', aliases=['name']), comment=dict(type='str')), supports_check_mode=True, mutually_exclusive=[['app', 'proto', 'logging']])
    cmds = []

    def execute(cmd):
        cmd = ' '.join(map(itemgetter((- 1)), filter(itemgetter(0), cmd)))
        cmds.append(cmd)
        (rc, out, err) = module.run_command(cmd)
        if (rc != 0):
            module.fail_json(msg=(err or out))

    def ufw_version():
        '\n        Returns the major and minor version of ufw installed on the system.\n        '
        (rc, out, err) = module.run_command(('%s --version' % ufw_bin))
        if (rc != 0):
            module.fail_json(msg='Failed to get ufw version.', rc=rc, out=out, err=err)
        lines = [x for x in out.split('\n') if (x.strip() != '')]
        if (len(lines) == 0):
            module.fail_json(msg='Failed to get ufw version.', rc=0, out=out)
        matches = re.search('^ufw.+(\\d+)\\.(\\d+)(?:\\.(\\d+))?.*$', lines[0])
        if (matches is None):
            module.fail_json(msg='Failed to get ufw version.', rc=0, out=out)
        major = int(matches.group(1))
        minor = int(matches.group(2))
        rev = 0
        if (matches.group(3) is not None):
            rev = int(matches.group(3))
        return (major, minor, rev)
    params = module.params
    command_keys = ['state', 'default', 'rule', 'logging']
    commands = dict(((key, params[key]) for key in command_keys if params[key]))
    if (len(commands) < 1):
        module.fail_json(msg=('Not any of the command arguments %s given' % commands))
    if ((params['interface'] is not None) and (params['direction'] is None)):
        module.fail_json(msg='Direction must be specified when creating a rule on an interface')
    ufw_bin = module.get_bin_path('ufw', True)
    (_, pre_state, _) = module.run_command((ufw_bin + ' status verbose'))
    (_, pre_rules, _) = module.run_command("grep '^### tuple' /lib/ufw/user.rules /lib/ufw/user6.rules /etc/ufw/user.rules /etc/ufw/user6.rules")
    for (command, value) in commands.items():
        cmd = [[ufw_bin], [module.check_mode, '--dry-run']]
        if (command == 'state'):
            states = {
                'enabled': 'enable',
                'disabled': 'disable',
                'reloaded': 'reload',
                'reset': 'reset',
            }
            execute((cmd + [['-f'], [states[value]]]))
        elif (command == 'logging'):
            execute((cmd + [[command], [value]]))
        elif (command == 'default'):
            execute((cmd + [[command], [value], [params['direction']]]))
        elif (command == 'rule'):
            cmd.append([module.boolean(params['route']), 'route'])
            cmd.append([module.boolean(params['delete']), 'delete'])
            cmd.append([params['insert'], ('insert %s' % params['insert'])])
            cmd.append([value])
            cmd.append([params['direction'], ('%s' % params['direction'])])
            cmd.append([params['interface'], ('on %s' % params['interface'])])
            cmd.append([module.boolean(params['log']), 'log'])
            for (key, template) in [('from_ip', 'from %s'), ('from_port', 'port %s'), ('to_ip', 'to %s'), ('to_port', 'port %s'), ('proto', 'proto %s'), ('app', "app '%s'")]:
                value = params[key]
                cmd.append([value, (template % value)])
            (ufw_major, ufw_minor, _) = ufw_version()
            if (((ufw_major == 0) and (ufw_minor >= 35)) or (ufw_major > 0)):
                cmd.append([params['comment'], ("comment '%s'" % params['comment'])])
            execute(cmd)
    (_, post_state, _) = module.run_command((ufw_bin + ' status verbose'))
    (_, post_rules, _) = module.run_command("grep '^### tuple' /lib/ufw/user.rules /lib/ufw/user6.rules /etc/ufw/user.rules /etc/ufw/user6.rules")
    changed = ((pre_state != post_state) or (pre_rules != post_rules))
    return module.exit_json(changed=changed, commands=cmds, msg=post_state.rstrip())