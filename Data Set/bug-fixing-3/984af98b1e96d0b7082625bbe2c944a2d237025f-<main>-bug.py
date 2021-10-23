def main():
    argument_spec = basic_auth_argument_spec()
    argument_spec.update(dict(name=dict(required=False, type='str'), ssid=dict(required=False, type='str'), current_password=dict(required=False, no_log=True), new_password=dict(required=True, no_log=True), set_admin=dict(required=True, type='bool'), api_url=dict(required=True), api_username=dict(required=False), api_password=dict(required=False, no_log=True)))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['name', 'ssid']], required_one_of=[['name', 'ssid']])
    name = module.params['name']
    ssid = module.params['ssid']
    current_password = module.params['current_password']
    new_password = module.params['new_password']
    set_admin = module.params['set_admin']
    user = module.params['api_username']
    pwd = module.params['api_password']
    api_url = module.params['api_url']
    if (not api_url.endswith('/')):
        api_url += '/'
    if name:
        ssid = get_ssid(module, name, api_url, user, pwd)
    (ro_pwd, admin_pwd) = get_pwd_status(module, ssid, api_url, user, pwd)
    if (admin_pwd and (not current_password)):
        module.fail_json(msg=('Admin account has a password set. ' + 'You must supply current_password in order to update the RO or Admin passwords'))
    if (len(new_password) > 30):
        module.fail_json(msg='Passwords must not be greater than 30 characters in length')
    success = set_password(module, ssid, api_url, user, pwd, current_password=current_password, new_password=new_password, set_admin=set_admin)
    module.exit_json(changed=True, msg='Password Updated Successfully', **success)