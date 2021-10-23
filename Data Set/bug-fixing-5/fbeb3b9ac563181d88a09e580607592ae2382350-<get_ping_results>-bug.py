def get_ping_results(command, module, transport):
    cmd = {
        'command': command,
        'output': 'text',
    }
    ping = run_commands(module, [cmd])[0]
    if (not ping):
        module.fail_json(msg='An unexpected error occurred. Check all params.', command=command, destination=module.params['dest'], vrf=module.params['vrf'], source=module.params['source'])
    elif ("can't bind to address" in ping):
        module.fail_json(msg="Can't bind to source address.", command=command)
    elif ('bad context' in ping):
        module.fail_json(msg='Wrong VRF name inserted.', command=command, vrf=module.params['vrf'])
    else:
        splitted_ping = ping.split('\n')
        reference_point = get_statistics_summary_line(splitted_ping)
        (summary, ping_pass) = get_summary(splitted_ping, reference_point)
        rtt = get_rtt(splitted_ping, summary['packet_loss'], (reference_point + 2))
    return (splitted_ping, summary, rtt, ping_pass)