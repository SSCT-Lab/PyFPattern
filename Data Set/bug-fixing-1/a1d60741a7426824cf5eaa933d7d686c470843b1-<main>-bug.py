

def main():
    argument_spec = dict(cas=dict(required=False), flags=dict(required=False), key=dict(required=True), host=dict(default='localhost'), scheme=dict(required=False, default='http'), validate_certs=dict(required=False, type='bool', default=True), port=dict(default=8500, type='int'), recurse=dict(required=False, type='bool'), retrieve=dict(required=False, type='bool', default=True), state=dict(default='present', choices=['present', 'absent', 'acquire', 'release']), token=dict(required=False, no_log=True), value=dict(required=False), session=dict(required=False))
    module = AnsibleModule(argument_spec, supports_check_mode=False)
    test_dependencies(module)
    try:
        execute(module)
    except ConnectionError as e:
        module.fail_json(msg=('Could not connect to consul agent at %s:%s, error was %s' % (module.params.get('host'), module.params.get('port'), str(e))))
    except Exception as e:
        module.fail_json(msg=str(e))
