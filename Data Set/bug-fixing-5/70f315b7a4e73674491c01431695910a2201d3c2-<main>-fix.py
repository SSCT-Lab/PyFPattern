def main():
    ' main entry point for module execution\n    '
    backup_spec = dict(filename=dict(), dir_path=dict(type='path'))
    argument_spec = dict(src=dict(type='path'), lines=dict(aliases=['commands'], type='list'), parents=dict(type='list'), before=dict(type='list'), after=dict(type='list'), match=dict(default='line', choices=['line', 'strict', 'exact', 'none']), replace=dict(default='line', choices=['line', 'block', 'config']), defaults=dict(type='bool', default=False), backup=dict(type='bool', default=False), backup_options=dict(type='dict', options=backup_spec), save_when=dict(choices=['always', 'never', 'modified', 'changed'], default='never'), diff_against=dict(choices=['startup', 'session', 'intended', 'running'], default='session'), diff_ignore_lines=dict(type='list'), running_config=dict(aliases=['config']), intended_config=dict())
    argument_spec.update(eos_argument_spec)
    mutually_exclusive = [('lines', 'src'), ('parents', 'src')]
    required_if = [('match', 'strict', ['lines']), ('match', 'exact', ['lines']), ('replace', 'block', ['lines']), ('replace', 'config', ['src']), ('diff_against', 'intended', ['intended_config'])]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, required_if=required_if, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    diff_ignore_lines = module.params['diff_ignore_lines']
    config = None
    contents = None
    flags = (['all'] if module.params['defaults'] else [])
    connection = get_connection(module)
    if (module.params['backup'] or (module._diff and (module.params['diff_against'] == 'running'))):
        contents = get_config(module, flags=flags)
        config = NetworkConfig(indent=1, contents=contents)
        if module.params['backup']:
            result['__backup__'] = contents
    if any((module.params['src'], module.params['lines'])):
        match = module.params['match']
        replace = module.params['replace']
        path = module.params['parents']
        candidate = get_candidate(module)
        running = get_running_config(module, contents, flags=flags)
        try:
            response = connection.get_diff(candidate=candidate, running=running, diff_match=match, diff_ignore_lines=diff_ignore_lines, path=path, diff_replace=replace)
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
        config_diff = response['config_diff']
        if config_diff:
            commands = config_diff.split('\n')
            if module.params['before']:
                commands[:0] = module.params['before']
            if module.params['after']:
                commands.extend(module.params['after'])
            result['commands'] = commands
            result['updates'] = commands
            replace = (module.params['replace'] == 'config')
            commit = (not module.check_mode)
            response = load_config(module, commands, replace=replace, commit=commit)
            result['changed'] = True
            if (module.params['diff_against'] == 'session'):
                if ('diff' in response):
                    result['diff'] = {
                        'prepared': response['diff'],
                    }
                else:
                    result['changed'] = False
            if ('session' in response):
                result['session'] = response['session']
    running_config = module.params['running_config']
    startup_config = None
    if (module.params['save_when'] == 'always'):
        save_config(module, result)
    elif (module.params['save_when'] == 'modified'):
        output = run_commands(module, [{
            'command': 'show running-config',
            'output': 'text',
        }, {
            'command': 'show startup-config',
            'output': 'text',
        }])
        running_config = NetworkConfig(indent=3, contents=output[0], ignore_lines=diff_ignore_lines)
        startup_config = NetworkConfig(indent=3, contents=output[1], ignore_lines=diff_ignore_lines)
        if (running_config.sha1 != startup_config.sha1):
            save_config(module, result)
    elif ((module.params['save_when'] == 'changed') and result['changed']):
        save_config(module, result)
    if module._diff:
        if (not running_config):
            output = run_commands(module, {
                'command': 'show running-config',
                'output': 'text',
            })
            contents = output[0]
        else:
            contents = running_config
        running_config = NetworkConfig(indent=3, contents=contents, ignore_lines=diff_ignore_lines)
        if (module.params['diff_against'] == 'running'):
            if module.check_mode:
                module.warn('unable to perform diff against running-config due to check mode')
                contents = None
            else:
                contents = config.config_text
        elif (module.params['diff_against'] == 'startup'):
            if (not startup_config):
                output = run_commands(module, {
                    'command': 'show startup-config',
                    'output': 'text',
                })
                contents = output[0]
            else:
                contents = startup_config.config_text
        elif (module.params['diff_against'] == 'intended'):
            contents = module.params['intended_config']
        if (contents is not None):
            base_config = NetworkConfig(indent=3, contents=contents, ignore_lines=diff_ignore_lines)
            if (running_config.sha1 != base_config.sha1):
                if (module.params['diff_against'] == 'intended'):
                    before = running_config
                    after = base_config
                elif (module.params['diff_against'] in ('startup', 'running')):
                    before = base_config
                    after = running_config
                result.update({
                    'changed': True,
                    'diff': {
                        'before': str(before),
                        'after': str(after),
                    },
                })
    module.exit_json(**result)