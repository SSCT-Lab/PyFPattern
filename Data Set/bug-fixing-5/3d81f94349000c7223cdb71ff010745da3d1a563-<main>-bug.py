def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(count=dict(type='int'), dest=dict(type='str', required=True), source=dict(type='str'), state=dict(type='str', choices=['absent', 'present'], default='present'), vrf=dict(type='str'))
    argument_spec.update(ios_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec)
    count = module.params['count']
    dest = module.params['dest']
    source = module.params['source']
    vrf = module.params['vrf']
    warnings = list()
    check_args(module, warnings)
    results = {
        
    }
    if warnings:
        results['warnings'] = warnings
    results['commands'] = [build_ping(dest, count, source, vrf)]
    ping_results = run_commands(module, commands=results['commands'])
    ping_results_list = ping_results[0].split('\n')
    (success, rx, tx, rtt) = parse_ping(ping_results_list[3])
    loss = abs((100 - int(success)))
    results['packet_loss'] = (str(loss) + '%')
    results['packets_rx'] = int(rx)
    results['packets_tx'] = int(tx)
    for (k, v) in rtt.items():
        if (rtt[k] is not None):
            rtt[k] = int(v)
    results['rtt'] = rtt
    validate_results(module, loss, results)
    module.exit_json(**results)