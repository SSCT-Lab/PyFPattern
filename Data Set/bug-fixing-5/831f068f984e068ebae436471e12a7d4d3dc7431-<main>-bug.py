def main():
    argument_spec = dict(name=dict(required=True), user=dict(), team=dict(), kind=dict(required=True, choices=KIND_CHOICES.keys()), host=dict(), username=dict(), password=dict(no_log=True), ssh_key_data=dict(no_log=True, type='str'), ssh_key_unlock=dict(no_log=True), authorize=dict(type='bool', default=False), authorize_password=dict(no_log=True), client=dict(), security_token=dict(), secret=dict(), tenant=dict(), subscription=dict(), domain=dict(), become_method=dict(), become_username=dict(), become_password=dict(no_log=True), vault_password=dict(no_log=True), description=dict(), organization=dict(required=True), project=dict(), state=dict(choices=['present', 'absent'], default='present'))
    module = TowerModule(argument_spec=argument_spec, supports_check_mode=True)
    name = module.params.get('name')
    organization = module.params.get('organization')
    state = module.params.get('state')
    json_output = {
        'credential': name,
        'state': state,
    }
    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        credential = tower_cli.get_resource('credential')
        try:
            params = {
                
            }
            params['create_on_missing'] = True
            params['name'] = name
            if organization:
                org_res = tower_cli.get_resource('organization')
                org = org_res.get(name=organization)
                params['organization'] = org['id']
            try:
                tower_cli.get_resource('credential_type')
            except (ImportError, AttributeError):
                params['kind'] = module.params['kind']
            else:
                credential_type = credential_type_for_v1_kind(module.params, module)
                params['credential_type'] = credential_type['id']
            if module.params.get('description'):
                params['description'] = module.params.get('description')
            if module.params.get('user'):
                user_res = tower_cli.get_resource('user')
                user = user_res.get(username=module.params.get('user'))
                params['user'] = user['id']
            if module.params.get('team'):
                team_res = tower_cli.get_resource('team')
                team = team_res.get(name=module.params.get('team'))
                params['team'] = team['id']
            if module.params.get('ssh_key_data'):
                data = module.params.get('ssh_key_data')
                if os.path.exists(data):
                    module.deprecate(msg="ssh_key_data should be a string, not a path to a file. Use lookup('file', '/path/to/file') instead", version='2.12')
                    if os.path.isdir(data):
                        module.fail_json(msg=('attempted to read contents of directory: %s' % data))
                    with open(data, 'rb') as f:
                        module.params['ssh_key_data'] = to_text(f.read())
                else:
                    module.params['ssh_key_data'] = data
            for key in ('authorize', 'authorize_password', 'client', 'security_token', 'secret', 'tenant', 'subscription', 'domain', 'become_method', 'become_username', 'become_password', 'vault_password', 'project', 'host', 'username', 'password', 'ssh_key_data', 'ssh_key_unlock'):
                if ('kind' in params):
                    params[key] = module.params.get(key)
                elif module.params.get(key):
                    params.setdefault('inputs', {
                        
                    })[key] = module.params.get(key)
            if (state == 'present'):
                result = credential.modify(**params)
                json_output['id'] = result['id']
            elif (state == 'absent'):
                result = credential.delete(**params)
        except exc.NotFound as excinfo:
            module.fail_json(msg='Failed to update credential, organization not found: {0}'.format(excinfo), changed=False)
        except (exc.ConnectionError, exc.BadRequest, exc.NotFound, exc.AuthError) as excinfo:
            module.fail_json(msg='Failed to update credential: {0}'.format(excinfo), changed=False)
    json_output['changed'] = result['changed']
    module.exit_json(**json_output)