

def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(src=dict(type='path'), lines=dict(aliases=['commands'], type='list'), parents=dict(type='list'), before=dict(type='list'), after=dict(type='list'), match=dict(default='line', choices=['line', 'strict', 'exact', 'none']), replace=dict(default='line', choices=['line', 'block']), multiline_delimiter=dict(default='@'), running_config=dict(aliases=['config']), intended_config=dict(), defaults=dict(type='bool', default=False), backup=dict(type='bool', default=False), save_when=dict(choices=['always', 'never', 'modified', 'changed'], default='never'), diff_against=dict(choices=['startup', 'intended', 'running']), diff_ignore_lines=dict(type='list'), save=dict(default=False, type='bool', removed_in_version='2.8'), force=dict(default=False, type='bool', removed_in_version='2.7'))
    argument_spec.update(ios_argument_spec)
    mutually_exclusive = [('lines', 'src'), ('parents', 'src'), ('save', 'save_when')]
    required_if = [('match', 'strict', ['lines']), ('match', 'exact', ['lines']), ('replace', 'block', ['lines']), ('diff_against', 'intended', ['intended_config'])]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, required_if=required_if, supports_check_mode=True)
    result = {
        'changed': False,
    }
    warnings = list()
    check_args(module, warnings)
    result['warnings'] = warnings
    config = None
    if (module.params['backup'] or (module._diff and (module.params['diff_against'] == 'running'))):
        contents = get_config(module)
        config = NetworkConfig(indent=1, contents=contents)
        if module.params['backup']:
            result['__backup__'] = contents
    if any((module.params['lines'], module.params['src'])):
        match = module.params['match']
        replace = module.params['replace']
        path = module.params['parents']
        (candidate, want_banners) = get_candidate(module)
        if (match != 'none'):
            (config, have_banners) = get_running_config(module, config)
            path = module.params['parents']
            configobjs = candidate.difference(config, path=path, match=match, replace=replace)
        else:
            configobjs = candidate.items
            have_banners = {
                
            }
        banners = diff_banners(want_banners, have_banners)
        if (configobjs or banners):
            commands = dumps(configobjs, 'commands').split('\n')
            if module.params['before']:
                commands[:0] = module.params['before']
            if module.params['after']:
                commands.extend(module.params['after'])
            result['commands'] = commands
            result['updates'] = commands
            result['banners'] = banners
            if (not module.check_mode):
                if commands:
                    load_config(module, commands)
                if banners:
                    load_banners(module, banners)
            result['changed'] = True
    running_config = None
    startup_config = None
    diff_ignore_lines = module.params['diff_ignore_lines']
    if ((module.params['save_when'] == 'always') or module.params['save']):
        save_config(module, result)
    elif (module.params['save_when'] == 'modified'):
        output = run_commands(module, ['show running-config', 'show startup-config'])
        running_config = NetworkConfig(indent=1, contents=output[0], ignore_lines=diff_ignore_lines)
        startup_config = NetworkConfig(indent=1, contents=output[1], ignore_lines=diff_ignore_lines)
        if (running_config.sha1 != startup_config.sha1):
            save_config(module, result)
    elif ((module.params['save_when'] == 'changed') and result['changed']):
        save_config(module, result)
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
                contents = startup_config.config_text
        elif (module.params['diff_against'] == 'intended'):
            contents = module.params['intended_config']
        if (contents is not None):
            base_config = NetworkConfig(indent=1, contents=contents, ignore_lines=diff_ignore_lines)
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
