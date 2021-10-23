def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(src=dict(type='path'), lines=dict(aliases=['commands'], type='list'), parents=dict(type='list'), before=dict(type='list'), after=dict(type='list'), match=dict(default='line', choices=['line', 'strict', 'exact', 'none']), replace=dict(default='line', choices=['line', 'block']), running_config=dict(aliases=['config']), intended_config=dict(), defaults=dict(type='bool', default=False), backup=dict(type='bool', default=False), save_when=dict(choices=['always', 'never', 'modified'], default='never'), diff_against=dict(choices=['running', 'startup', 'intended']), diff_ignore_lines=dict(type='list'), save=dict(default=False, type='bool', removed_in_version='2.4'), force=dict(default=False, type='bool', removed_in_version='2.2'))
    argument_spec.update(nxos_argument_spec)
    mutually_exclusive = [('lines', 'src'), ('save', 'save_when')]
    required_if = [('match', 'strict', ['lines']), ('match', 'exact', ['lines']), ('replace', 'block', ['lines']), ('diff_against', 'intended', ['intended_config'])]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, required_if=required_if, supports_check_mode=True)
    warnings = list()
    nxos_check_args(module, warnings)
    result = {
        'changed': False,
        'warnings': warnings,
    }
    config = None
    if (module.params['backup'] or (module._diff and (module.params['diff_against'] == 'running'))):
        contents = get_config(module)
        config = NetworkConfig(indent=2, contents=contents)
        if module.params['backup']:
            result['__backup__'] = contents
    if any((module.params['src'], module.params['lines'])):
        match = module.params['match']
        replace = module.params['replace']
        candidate = get_candidate(module)
        if (match != 'none'):
            config = get_running_config(module, config)
            path = module.params['parents']
            configobjs = candidate.difference(config, match=match, replace=replace, path=path)
        else:
            configobjs = candidate.items
        if configobjs:
            commands = dumps(configobjs, 'commands').split('\n')
            if module.params['before']:
                commands[:0] = module.params['before']
            if module.params['after']:
                commands.extend(module.params['after'])
            result['commands'] = commands
            result['updates'] = commands
            if (not module.check_mode):
                load_config(module, commands)
            result['changed'] = True
    running_config = None
    startup_config = None
    diff_ignore_lines = module.params['diff_ignore_lines']
    if (module.params['save_when'] != 'never'):
        output = run_commands(module, ['show running-config', 'startup-config'])
        running_config = NetworkConfig(indent=1, contents=output[0], ignore_lines=diff_ignore_lines)
        startup_config = NetworkConfig(indent=1, contents=output[1], ignore_lines=diff_ignore_lines)
        if ((running_config.sha1 != startup_config.sha1) or (module.params['save_when'] == 'always')):
            result['changed'] = True
            if (not module.check_mode):
                cmd = {
                    'command': 'copy running-config startup-config',
                    'output': 'text',
                }
                run_commands(module, [cmd])
            else:
                module.warn('Skipping command `copy running-config startup-config` due to check_mode.  Configuration not copied to non-volatile storage')
    if module._diff:
        if (not running_config):
            output = run_commands(module, 'show running-config')
            contents = output[0]
        else:
            contents = running_config.config_text
        running_config = NetworkConfig(indent=1, contents=contents, ignore_lines=diff_ignore_lines)
        if (module.params['diff_against'] == 'running'):
            if module.check_mode:
                module.warn('unable to perform diff against running-config due to check mode')
                contents = None
            else:
                contents = config.config_text
        elif (module.params['diff_against'] == 'startup'):
            if (not startup_config):
                output = run_commands(module, 'show startup-config')
                contents = output[0]
            else:
                contents = output[0]
                contents = startup_config.config_text
        elif (module.params['diff_against'] == 'intended'):
            contents = module.params['intended_config']
        if (contents is not None):
            base_config = NetworkConfig(indent=1, contents=contents, ignore_lines=diff_ignore_lines)
            if (running_config.sha1 != base_config.sha1):
                result.update({
                    'changed': True,
                    'diff': {
                        'before': str(base_config),
                        'after': str(running_config),
                    },
                })
    module.exit_json(**result)