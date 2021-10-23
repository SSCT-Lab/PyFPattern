

def run(module, result):
    match = module.params['match']
    replace = module.params['replace']
    path = module.params['parents']
    candidate = get_candidate(module)
    if (match != 'none'):
        config = get_config(module)
        configobjs = candidate.difference(config, path=path, match=match, replace=replace)
    else:
        configobjs = candidate.items
    if configobjs:
        commands = dumps(configobjs, 'commands').split('\n')
        if module.params['lines']:
            if module.params['before']:
                commands[:0] = module.params['before']
            if module.params['after']:
                commands.extend(module.params['after'])
        result['updates'] = commands
        if (not module.check_mode):
            result['responses'] = module.config.load_config(commands)
        result['changed'] = True
    if module.params['save']:
        if (not module.check_mode):
            module.config.save_config()
        result['changed'] = True
