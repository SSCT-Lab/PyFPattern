def main():
    module = AnsibleModule(argument_spec=dict(cas=dict(type='str'), flags=dict(type='str'), key=dict(type='str', required=True), host=dict(type='str', default='localhost'), scheme=dict(type='str', default='http'), validate_certs=dict(type='bool', default=True), port=dict(type='int', default=8500), recurse=dict(type='bool'), retrieve=dict(type='bool', default=True), state=dict(type='str', default='present', choices=['absent', 'acquire', 'present', 'release']), token=dict(type='str', no_log=True), value=dict(type='str', default=NOT_SET), session=dict(type='str')), supports_check_mode=False)
    test_dependencies(module)
    try:
        execute(module)
    except ConnectionError as e:
        module.fail_json(msg=('Could not connect to consul agent at %s:%s, error was %s' % (module.params.get('host'), module.params.get('port'), e)))
    except Exception as e:
        module.fail_json(msg=str(e))