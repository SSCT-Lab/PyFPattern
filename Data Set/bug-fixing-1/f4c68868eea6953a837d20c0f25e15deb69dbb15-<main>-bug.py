

def main():
    module = AnsibleModule(argument_spec=dict(url=dict(default=None), username=dict(default=None), password=dict(default=None, no_log=True), ca_file=dict(default=None, type='path'), insecure=dict(required=False, type='bool', default=False), timeout=dict(required=False, type='int', default=0), compress=dict(required=False, type='bool', default=True), kerberos=dict(required=False, type='bool', default=False), headers=dict(required=False, type='dict'), state=dict(default='present', choices=['present', 'absent']), token=dict(default=None), ovirt_auth=dict(required=None, type='dict')), required_if=[('state', 'absent', ['ovirt_auth'])], supports_check_mode=True)
    check_sdk(module)
    state = module.params.get('state')
    if (state == 'present'):
        params = module.params
    elif (state == 'absent'):
        params = module.params['ovirt_auth']
    url = (params.get('url') or os.environ.get('OVIRT_URL'))
    username = (params.get('username') or os.environ.get('OVIRT_USERNAME'))
    password = (params.get('password') or os.environ.get('OVIRT_PASSWORD'))
    ca_file = (params.get('ca_file') or os.environ.get('OVIRT_CAFILE'))
    insecure = (params.get('insecure') or (ca_file is None))
    token = (params.get('token') or os.environ.get('OVIRT_TOKEN'))
    connection = sdk.Connection(url=url, username=username, password=password, ca_file=ca_file, insecure=insecure, timeout=params.get('timeout'), compress=params.get('compress'), kerberos=params.get('kerberos'), headers=params.get('headers'), token=token)
    try:
        token = connection.authenticate()
        module.exit_json(changed=False, ansible_facts=dict(ovirt_auth=(dict(token=token, url=url, ca_file=ca_file, insecure=insecure, timeout=params.get('timeout'), compress=params.get('compress'), kerberos=params.get('kerberos'), headers=params.get('headers')) if (state == 'present') else dict())))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(state == 'absent'))
