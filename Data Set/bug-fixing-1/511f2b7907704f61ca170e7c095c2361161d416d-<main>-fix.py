

def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(lines=dict(type='list'), src=dict(type='path'), src_format=dict(choices=['xml', 'text', 'set', 'json']), update=dict(default='merge', choices=['merge', 'overwrite', 'replace']), replace=dict(default=False, type='bool'), confirm=dict(default=0, type='int'), comment=dict(default=DEFAULT_COMMENT), backup=dict(type='bool', default=False), rollback=dict(type='int'), zeroize=dict(default=False, type='bool'), transport=dict(default='netconf', choices=['netconf']))
    mutually_exclusive = [('lines', 'rollback'), ('lines', 'zeroize'), ('rollback', 'zeroize'), ('lines', 'src'), ('src', 'zeroize'), ('src', 'rollback'), ('update', 'replace')]
    required_if = [('replace', True, ['src']), ('update', 'merge', ['src', 'lines'], True), ('update', 'overwrite', ['src', 'lines'], True), ('update', 'replace', ['src', 'lines'], True)]
    module = NetworkModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, required_if=required_if, supports_check_mode=True)
    result = dict(changed=False)
    if module.params['backup']:
        result['__backup__'] = module.config.get_config()
    try:
        run(module, result)
    except NetworkError:
        exc = get_exception()
        module.fail_json(msg=str(exc), **exc.kwargs)
    module.exit_json(**result)
