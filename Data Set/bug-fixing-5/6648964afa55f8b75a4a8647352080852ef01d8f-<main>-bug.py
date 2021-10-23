def main():
    module = AnsibleModule(argument_spec=dict(url=dict(default=None), username=dict(default=None), password=dict(default=None, no_log=True), ca_file=dict(default=None, type='path'), insecure=dict(required=False, type='bool', default=False), timeout=dict(required=False, type='int', default=0), compress=dict(required=False, type='bool', default=True), kerberos=dict(required=False, type='bool', default=False), headers=dict(required=False, type='dict'), state=dict(default='present', choices=['present', 'absent']), ovirt_auth=dict(required=None, type='dict')), required_if=[('state', 'absent', ['ovirt_auth']), ('state', 'present', ['username', 'password', 'url'])], supports_check_mode=True)
    check_sdk(module)
    state = module.params.get('state')
    if (state == 'present'):
        params = module.params
    elif (state == 'absent'):
        params = module.params['ovirt_auth']
    connection = sdk.Connection(url=params.get('url'), username=params.get('username'), password=params.get('password'), ca_file=params.get('ca_file'), insecure=params.get('insecure'), timeout=params.get('timeout'), compress=params.get('compress'), kerberos=params.get('kerberos'), headers=params.get('headers'), token=params.get('token'))
    try:
        token = connection.authenticate()
        module.exit_json(changed=False, ansible_facts=dict(ovirt_auth=(dict(token=token, url=params.get('url'), ca_file=params.get('ca_file'), insecure=params.get('insecure'), timeout=params.get('timeout'), compress=params.get('compress'), kerberos=params.get('kerberos'), headers=params.get('headers')) if (state == 'present') else dict())))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(state == 'absent'))