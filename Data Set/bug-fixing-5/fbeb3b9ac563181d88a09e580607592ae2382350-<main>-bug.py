def main():
    argument_spec = dict(dest=dict(required=True), count=dict(required=False, default=2), vrf=dict(required=False), source=dict(required=False), state=dict(required=False, choices=['present', 'absent'], default='present'), include_defaults=dict(default=False), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    destination = module.params['dest']
    count = module.params['count']
    vrf = module.params['vrf']
    source = module.params['source']
    state = module.params['state']
    if count:
        try:
            if ((int(count) < 1) or (int(count) > 655350)):
                raise ValueError
        except ValueError:
            module.fail_json(msg="'count' must be an integer between 1 and 655350.", count=count)
    OPTIONS = {
        'vrf': vrf,
        'count': count,
        'source': source,
    }
    ping_command = 'ping {0}'.format(destination)
    for (command, arg) in OPTIONS.items():
        if arg:
            ping_command += ' {0} {1}'.format(command, arg)
    (ping_results, summary, rtt, ping_pass) = get_ping_results(ping_command, module, module.params['transport'])
    packet_loss = summary['packet_loss']
    packets_rx = summary['packets_rx']
    packets_tx = summary['packets_tx']
    results = {
        
    }
    results['updates'] = [ping_command]
    results['action'] = ping_results[1]
    results['dest'] = destination
    results['count'] = count
    results['packets_tx'] = packets_tx
    results['packets_rx'] = packets_rx
    results['packet_loss'] = packet_loss
    results['rtt'] = rtt
    results['state'] = module.params['state']
    if (ping_pass and (state == 'absent')):
        module.fail_json(msg='Ping succeeded unexpectedly', results=results)
    elif ((not ping_pass) and (state == 'present')):
        module.fail_json(msg='Ping failed unexpectedly', results=results)
    else:
        module.exit_json(**results)