def run(module, result):
    match = module.params['match']
    candidate = get_candidate(module)
    if (match != 'none'):
        config_text = get_active_config(module)
        config = NetworkConfig(indent=4, contents=config_text)
        configobjs = candidate.difference(config)
    else:
        configobjs = candidate.items
    if configobjs:
        commands = dumps(configobjs, 'commands')
        commands = commands.split('\n')
        result['commands'] = commands
        result['updates'] = commands
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True