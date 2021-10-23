def run(module, result):
    match = module.params['match']
    replace = module.params['replace']
    candidate = get_candidate(module)
    if (match != 'none'):
        config = get_running_config(module)
        path = module.params['parents']
        configobjs = candidate.difference(config, match=match, replace=replace, path=path)
    else:
        configobjs = candidate.items
    if configobjs:
        commands = dumps(configobjs, 'commands').split('\n')
        if module.params['lines']:
            commands = conversion_lines(commands)
            if module.params['before']:
                commands[:0] = module.params['before']
            if module.params['after']:
                commands.extend(module.params['after'])
        command_display = []
        for per_command in commands:
            if (per_command.strip() not in ['quit', 'return', 'system-view']):
                command_display.append(per_command)
        result['commands'] = command_display
        result['updates'] = command_display
        if (not module.check_mode):
            load_config(module, commands)
        if result['commands']:
            result['changed'] = True