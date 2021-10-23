def main():
    '\n    Main entry point for module execution\n    '
    argument_spec = dict(netbox_url=dict(type='str', required=True), netbox_token=dict(type='str', required=True, no_log=True), data=dict(type='dict', required=True), state=dict(required=False, default='present', choices=['present', 'absent']), validate_certs=dict(type='bool', default=True))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_PYNETBOX):
        module.fail_json(msg='pynetbox is required for this module')
    app = 'dcim'
    endpoint = 'devices'
    url = module.params['netbox_url']
    token = module.params['netbox_token']
    data = module.params['data']
    state = module.params['state']
    validate_certs = module.params['validate_certs']
    try:
        nb = pynetbox.api(url, token=token, ssl_verify=validate_certs)
    except Exception:
        module.fail_json(msg='Failed to establish connection to Netbox API')
    try:
        nb_app = getattr(nb, app)
    except AttributeError:
        module.fail_json(msg=('Incorrect application specified: %s' % app))
    nb_endpoint = getattr(nb_app, endpoint)
    norm_data = normalize_data(data)
    try:
        if ('present' in state):
            return module.exit_json(**ensure_device_present(nb, nb_endpoint, norm_data))
        else:
            return module.exit_json(**ensure_device_absent(nb_endpoint, norm_data))
    except pynetbox.RequestError as e:
        return module.fail_json(msg=json.loads(e.error))