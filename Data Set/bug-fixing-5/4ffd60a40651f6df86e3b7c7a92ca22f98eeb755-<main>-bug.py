def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), state=dict(choices=['started', 'stopped', 'reset', 'restarted', 'reloaded'], type='str'), enabled=dict(type='bool'), preset=dict(type='bool'), user=dict(type='bool')), supports_check_mode=True, mutually_exclusive=[['enabled', 'preset']])
    service = module.params['name']
    rc = 0
    out = err = ''
    result = {
        'name': service,
        'changed': False,
        'status': {
            
        },
    }
    service_path = get_service_path(module, service)
    result['service_path'] = service_path
    if ((module.params['enabled'] is not None) or module.params['preset']):
        handle_enabled(module, result, service_path)
    if (module.params['state'] is not None):
        handle_state(module, result, service_path)
    if service_is_loaded(module, service_path):
        result['status'] = get_service_status(module, service_path)
    else:
        result['status'] = {
            'Loaded': False,
        }
    module.exit_json(**result)