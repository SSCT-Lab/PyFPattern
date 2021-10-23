def main():
    'main entry point for execution\n    '
    argument_spec = dict(backup=dict(default=False, type='bool'), config=dict(type='str'), commit=dict(type='bool'), replace=dict(type='str'), rollback=dict(type='int'), commit_comment=dict(type='str'), defaults=dict(default=False, type='bool'), multiline_delimiter=dict(type='str'), diff_replace=dict(choices=['line', 'block', 'config']), diff_match=dict(choices=['line', 'strict', 'exact', 'none']), diff_ignore_lines=dict(type='list'))
    mutually_exclusive = [('config', 'rollback')]
    required_one_of = [['backup', 'config', 'rollback']]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, required_one_of=required_one_of, supports_check_mode=True)
    result = {
        'changed': False,
    }
    connection = Connection(module._socket_path)
    capabilities = module.from_json(connection.get_capabilities())
    if capabilities:
        validate_args(module, capabilities)
    if module.params['defaults']:
        if ('get_default_flag' in capabilities.get('rpc')):
            flags = connection.get_default_flag()
        else:
            flags = 'all'
    else:
        flags = []
    candidate = to_text(module.params['config'])
    running = connection.get_config(flags=flags)
    if module.params['backup']:
        result['__backup__'] = running
    try:
        result.update(run(module, capabilities, connection, candidate, running))
    except Exception as exc:
        module.fail_json(msg=to_text(exc))
    module.exit_json(**result)