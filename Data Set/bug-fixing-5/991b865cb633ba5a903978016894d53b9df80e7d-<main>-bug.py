def main():
    ' main entry point for module execution\n    '
    backup_spec = dict(filename=dict(), dir_path=dict(type='path'))
    argument_spec = dict(lines=dict(type='list'), src=dict(type='path'), src_format=dict(choices=['xml', 'text', 'set', 'json']), update=dict(default='merge', choices=['merge', 'override', 'replace', 'update']), replace=dict(type='bool'), confirm=dict(default=0, type='int'), comment=dict(default=DEFAULT_COMMENT), confirm_commit=dict(type='bool', default=False), check_commit=dict(type='bool', default=False), backup=dict(type='bool', default=False), backup_options=dict(type='dict', options=backup_spec), rollback=dict(type='int'), zeroize=dict(default=False, type='bool'))
    argument_spec.update(junos_argument_spec)
    mutually_exclusive = [('lines', 'src', 'rollback', 'zeroize')]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    candidate = (module.params['lines'] or module.params['src'])
    commit = (not module.check_mode)
    result = {
        'changed': False,
        'warnings': warnings,
    }
    if module.params['backup']:
        for conf_format in ['set', 'text']:
            reply = get_configuration(module, format=conf_format)
            match = reply.find(('.//configuration-%s' % conf_format))
            if (match is not None):
                break
        else:
            module.fail_json(msg='unable to retrieve device configuration')
        result['__backup__'] = match.text.strip()
    rollback_id = module.params['rollback']
    if rollback_id:
        diff = rollback(module, rollback_id)
        if commit:
            kwargs = {
                'comment': module.params['comment'],
            }
            with locked_config(module):
                load_configuration(module, rollback=rollback_id)
                commit_configuration(module, **kwargs)
            if module._diff:
                result['diff'] = {
                    'prepared': diff,
                }
        result['changed'] = True
    elif module.params['zeroize']:
        if commit:
            zeroize(module)
        result['changed'] = True
    elif candidate:
        with locked_config(module):
            diff = configure_device(module, warnings, candidate)
            if diff:
                if commit:
                    kwargs = {
                        'comment': module.params['comment'],
                        'check': module.params['check_commit'],
                    }
                    confirm = module.params['confirm']
                    if (confirm > 0):
                        kwargs.update({
                            'confirm': True,
                            'confirm_timeout': to_text(confirm, errors='surrogate_then_replace'),
                        })
                    commit_configuration(module, **kwargs)
                else:
                    discard_changes(module)
                result['changed'] = True
                if module._diff:
                    result['diff'] = {
                        'prepared': diff,
                    }
    elif module.params['check_commit']:
        commit_configuration(module, check=True)
    elif module.params['confirm_commit']:
        with locked_config(module):
            commit_configuration(module)
        result['changed'] = True
    module.exit_json(**result)