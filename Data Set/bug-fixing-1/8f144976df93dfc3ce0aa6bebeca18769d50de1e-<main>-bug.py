

def main():
    module = AnsibleModule(argument_spec=dict(url=dict(default=None), hostname=dict(default=None), username=dict(default=None), password=dict(default=None, no_log=True), ca_file=dict(default=None, type='path'), insecure=dict(required=False, type='bool', default=None), timeout=dict(required=False, type='int', default=0), compress=dict(required=False, type='bool', default=True), kerberos=dict(required=False, type='bool', default=False), headers=dict(required=False, type='dict'), state=dict(default='present', choices=['present', 'absent']), token=dict(default=None), ovirt_auth=dict(required=None, type='dict')), required_if=[('state', 'absent', ['ovirt_auth'])], supports_check_mode=True)
    check_sdk(module)
    state = module.params.get('state')
    if (state == 'present'):
        params = module.params
    elif (state == 'absent'):
        params = module.params['ovirt_auth']

    def get_required_parameter(param, env_var, required=False):
        var = (params.get(param) or os.environ.get(env_var))
        if ((not var) and required and (state == 'present')):
            module.fail_json(msg=("'%s' is a required parameter." % param))
        return var
    url = get_required_parameter('url', 'OVIRT_URL', required=False)
    hostname = get_required_parameter('hostname', 'OVIRT_HOSTNAME', required=False)
    if ((url is None) and (hostname is None)):
        module.fail_json(msg="You must specify either 'url' or 'hostname'.")
    if ((url is None) and (hostname is not None)):
        url = 'https://{0}/ovirt-engine/api'.format(hostname)
    username = get_required_parameter('username', 'OVIRT_USERNAME', required=True)
    password = get_required_parameter('password', 'OVIRT_PASSWORD', required=True)
    token = get_required_parameter('token', 'OVIRT_TOKEN')
    ca_file = get_required_parameter('ca_file', 'OVIRT_CAFILE')
    insecure = (params.get('insecure') if (params.get('insecure') is not None) else (not bool(ca_file)))
    connection = sdk.Connection(url=url, username=username, password=password, ca_file=ca_file, insecure=insecure, timeout=params.get('timeout'), compress=params.get('compress'), kerberos=params.get('kerberos'), headers=params.get('headers'), token=token)
    try:
        token = connection.authenticate()
        module.exit_json(changed=False, ansible_facts=dict(ovirt_auth=(dict(token=token, url=url, ca_file=ca_file, insecure=insecure, timeout=params.get('timeout'), compress=params.get('compress'), kerberos=params.get('kerberos'), headers=params.get('headers')) if (state == 'present') else dict())))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(state == 'absent'))
