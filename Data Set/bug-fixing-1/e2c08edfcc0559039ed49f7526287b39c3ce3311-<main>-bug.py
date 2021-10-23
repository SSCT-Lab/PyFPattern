

def main():
    module = AnsibleModule(argument_spec=dict(username=dict(required=True), first_name=dict(), last_name=dict(), password=dict(no_log=True), email=dict(required=True), organization=dict(), superuser=dict(type='bool', default=False), auditor=dict(type='bool', default=False), tower_host=dict(), tower_username=dict(), tower_password=dict(no_log=True), tower_verify_ssl=dict(type='bool', default=True), tower_config_file=dict(type='path'), state=dict(choices=['present', 'absent'], default='present')), supports_check_mode=True)
    if (not HAS_TOWER_CLI):
        module.fail_json(msg='ansible-tower-cli required for this module')
    username = module.params.get('username')
    first_name = module.params.get('first_name')
    last_name = module.params.get('last_name')
    password = module.params.get('password')
    email = module.params.get('email')
    organization = module.params.get('organization')
    superuser = module.params.get('superuser')
    auditor = module.params.get('auditor')
    state = module.params.get('state')
    json_output = {
        'username': username,
        'state': state,
    }
    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        user = tower_cli.get_resource('user')
        try:
            if (state == 'present'):
                result = user.modify(username=username, first_name=first_name, last_name=last_name, email=email, password=password, organization=organization, is_superuser=superuser, is_auditor=auditor, create_on_missing=True)
                json_output['id'] = result['id']
            elif (state == 'absent'):
                result = user.delete(username=username)
        except (exc.ConnectionError, exc.BadRequest) as excinfo:
            module.fail_json(msg='Failed to update the user: {0}'.format(excinfo), changed=False)
    json_output['changed'] = result['changed']
    module.exit_json(**json_output)
