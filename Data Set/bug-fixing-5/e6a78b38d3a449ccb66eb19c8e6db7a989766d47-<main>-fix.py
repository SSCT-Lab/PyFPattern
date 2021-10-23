def main():
    'main entry point for module execution\n    '
    argument_spec = dict(src=dict(type='path'), lines=dict(aliases=['commands'], type='list'), parents=dict(type='list'), before=dict(type='list'), after=dict(type='list'), match=dict(default='line', choices=['line', 'strict', 'exact', 'none']), replace=dict(default='line', choices=['line', 'block', 'config']), force=dict(default=False, type='bool'), config=dict(), backup=dict(type='bool', default=False), comment=dict(default=DEFAULT_COMMIT_COMMENT))
    argument_spec.update(iosxr_argument_spec)
    mutually_exclusive = [('lines', 'src')]
    required_if = [('match', 'strict', ['lines']), ('match', 'exact', ['lines']), ('replace', 'block', ['lines']), ('replace', 'config', ['src'])]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, required_if=required_if, supports_check_mode=True)
    if (module.params['force'] is True):
        module.params['match'] = 'none'
    warnings = list()
    check_args(module, warnings)
    result = dict(changed=False, warnings=warnings)
    if module.params['backup']:
        result['__backup__'] = get_config(module)
    run(module, result)
    module.exit_json(**result)