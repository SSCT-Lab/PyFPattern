def main():
    argument_spec = dict(dest=dict(required=True), count=dict(required=False, default=5), vrf=dict(required=False), source=dict(required=False), state=dict(required=False, choices=['present', 'absent'], default='present'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    destination = module.params['dest']
    count = module.params['count']
    state = module.params['state']
    ping_command = 'ping {0}'.format(destination)
    for command in ['count', 'source', 'vrf']:
        arg = module.params[command]
        if arg:
            ping_command += ' {0} {1}'.format(command, arg)
    (summary, rtt, ping_pass) = get_ping_results(ping_command, module)
    results = summary
    results['rtt'] = rtt
    results['commands'] = [ping_command]
    if (ping_pass and (state == 'absent')):
        module.fail_json(msg='Ping succeeded unexpectedly')
    elif ((not ping_pass) and (state == 'present')):
        module.fail_json(msg='Ping failed unexpectedly')
    module.exit_json(**results)