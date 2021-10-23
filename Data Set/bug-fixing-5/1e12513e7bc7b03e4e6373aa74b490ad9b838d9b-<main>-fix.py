def main():
    '\n    Main entry point for module execution\n    '
    argument_spec = dict(netbox_url=dict(type='str', required=True), netbox_token=dict(type='str', required=True, no_log=True), data=dict(type='dict', required=True), state=dict(required=False, default='present', choices=['present', 'absent', 'new']), validate_certs=dict(type='bool', default=True))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_PYNETBOX):
        module.fail_json(msg=missing_required_lib('pynetbox'), exception=PYNETBOX_IMP_ERR)
    changed = False
    app = 'ipam'
    endpoint = 'ip_addresses'
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
        norm_data = _check_and_adapt_data(nb, norm_data)
        if (state in ('new', 'present')):
            return _handle_state_new_present(module, state, nb_app, nb_endpoint, norm_data)
        elif (state == 'absent'):
            return module.exit_json(**ensure_ip_address_absent(nb_endpoint, norm_data))
        else:
            return module.fail_json(msg=('Invalid state %s' % state))
    except pynetbox.RequestError as e:
        return module.fail_json(msg=json.loads(e.error))
    except ValueError as e:
        return module.fail_json(msg=str(e))