

def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(lines=dict(type='list'), src=dict(type='path'), src_format=dict(choices=['xml', 'text', 'set', 'json']), update=dict(default='merge', choices=['merge', 'override', 'replace', 'update']), replace=dict(type='bool'), confirm=dict(default=0, type='int'), comment=dict(default=DEFAULT_COMMENT), backup=dict(type='bool', default=False), rollback=dict(type='int'), zeroize=dict(default=False, type='bool'))
    argument_spec.update(junos_argument_spec)
    mutually_exclusive = [('lines', 'src', 'rollback', 'zeroize')]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
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
        result['__backup__'] = str(match.text).strip()
    if module.params['rollback']:
        if (not module.check_mode):
            diff = rollback(module)
            if module._diff:
                result['diff'] = {
                    'prepared': diff,
                }
        result['changed'] = True
    elif module.params['zeroize']:
        if (not module.check_mode):
            zeroize(module)
        result['changed'] = True
    else:
        diff = configure_device(module, warnings)
        if diff:
            if module._diff:
                result['diff'] = {
                    'prepared': diff,
                }
            result['changed'] = True
    module.exit_json(**result)
