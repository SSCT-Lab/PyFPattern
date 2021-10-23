def get_current(module):
    cmd = ('show running-config', 'show ntp logging')
    output = run_commands(module, ({
        'command': cmd[0],
        'output': 'text',
    }, {
        'command': cmd[1],
        'output': 'text',
    }))
    match = re.search('^ntp master(?: (\\d+))', output[0], re.M)
    if match:
        master = True
        stratum = match.group(1)
    else:
        master = False
        stratum = None
    logging = ('Enabled' in output[1])
    return {
        'master': master,
        'stratum': stratum,
        'logging': logging,
    }