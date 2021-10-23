

def main():
    argument_spec = dict(user=dict(), team=dict(), role=dict(choices=['admin', 'read', 'member', 'execute', 'adhoc', 'update', 'use', 'auditor']), target_team=dict(), inventory=dict(), job_template=dict(), credential=dict(), organization=dict(), project=dict(), state=dict(choices=['present', 'absent'], default='present'))
    module = TowerModule(argument_spec=argument_spec, supports_check_mode=True)
    role_type = module.params.pop('role')
    state = module.params.pop('state')
    json_output = {
        'role': role_type,
        'state': state,
    }
    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        role = tower_cli.get_resource('role')
        params = update_resources(module, module.params)
        params['type'] = role_type
        try:
            if (state == 'present'):
                result = role.grant(**params)
                json_output['id'] = result['id']
            elif (state == 'absent'):
                result = role.revoke(**params)
        except (exc.ConnectionError, exc.BadRequest, exc.NotFound, exc.AuthError) as excinfo:
            module.fail_json(msg='Failed to update role: {0}'.format(excinfo), changed=False)
    json_output['changed'] = result['changed']
    module.exit_json(**json_output)
