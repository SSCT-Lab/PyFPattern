

def main():
    argument_spec = dict(lines=dict(aliases=['commands'], type='list'), parents=dict(type='list'), src=dict(type='path'), before=dict(type='list'), after=dict(type='list'), match=dict(default='line', choices=['line', 'strict', 'exact', 'none']), replace=dict(default='line', choices=['line', 'block']), update=dict(choices=['merge', 'check'], default='merge'), save=dict(type='bool', default=False), config=dict(), backup=dict(type='bool', default=False))
    argument_spec.update(dellos6_argument_spec)
    mutually_exclusive = [('lines', 'src'), ('parents', 'src')]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    parents = (module.params['parents'] or list())
    match = module.params['match']
    replace = module.params['replace']
    warnings = list()
    check_args(module, warnings)
    result = dict(changed=False, saved=False, warnings=warnings)
    candidate = get_candidate(module)
    if module.params['backup']:
        if (not module.check_mode):
            result['__backup__'] = get_config(module)
    commands = list()
    if any((module.params['lines'], module.params['src'])):
        if (match != 'none'):
            config = get_running_config(module)
            config = Dellos6NetworkConfig(contents=config, indent=0)
            if parents:
                config = get_sublevel_config(config, module)
            configobjs = candidate.difference(config, match=match, replace=replace)
        else:
            configobjs = candidate.items
        if configobjs:
            commands = dumps(configobjs, 'commands')
            if (isinstance(module.params['lines'], list) and isinstance(module.params['lines'][0], dict) and set(['prompt', 'answer']).issubset(module.params['lines'][0])):
                cmd = {
                    'command': commands,
                    'prompt': module.params['lines'][0]['prompt'],
                    'answer': module.params['lines'][0]['answer'],
                }
                commands = [module.jsonify(cmd)]
            else:
                commands = commands.split('\n')
            if module.params['before']:
                commands[:0] = module.params['before']
            if module.params['after']:
                commands.extend(module.params['after'])
            if ((not module.check_mode) and (module.params['update'] == 'merge')):
                load_config(module, commands)
            result['changed'] = True
            result['commands'] = commands
            result['updates'] = commands
    if module.params['save']:
        result['changed'] = True
        if (not module.check_mode):
            cmd = {
                'command': 'copy running-config startup-config',
                'prompt': '\\(y/n\\)\\s?$',
                'answer': 'yes',
            }
            run_commands(module, [cmd])
            result['saved'] = True
        else:
            module.warn('Skipping command `copy running-config startup-config`due to check_mode.  Configuration not copied to non-volatile storage')
    module.exit_json(**result)
