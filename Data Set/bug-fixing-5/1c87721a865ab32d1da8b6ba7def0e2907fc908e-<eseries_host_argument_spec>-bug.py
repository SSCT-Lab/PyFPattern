def eseries_host_argument_spec():
    'Retrieve a base argument specifiation common to all NetApp E-Series modules'
    argument_spec = basic_auth_argument_spec()
    argument_spec.update(dict(api_username=dict(type='str', required=True), api_password=dict(type='str', required=True, no_log=True), api_url=dict(type='str', required=True), ssid=dict(type='str', required=True), validate_certs=dict(required=False, default=True)))
    return argument_spec