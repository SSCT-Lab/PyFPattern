def main():
    argument_spec = tower_argument_spec()
    argument_spec.update(dict(name=dict(required=True), description=dict(), organization=dict(required=True), variables=dict(), state=dict(choices=['present', 'absent'], default='present')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_TOWER_CLI):
        module.fail_json(msg='ansible-tower-cli required for this module')
    name = module.params.get('name')
    description = module.params.get('description')
    organization = module.params.get('organization')
    variables = module.params.get('variables')
    state = module.params.get('state')
    json_output = {
        'inventory': name,
        'state': state,
    }
    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        inventory = tower_cli.get_resource('inventory')
        try:
            org_res = tower_cli.get_resource('organization')
            org = org_res.get(name=organization)
            if (state == 'present'):
                result = inventory.modify(name=name, organization=org['id'], variables=variables, description=description, create_on_missing=True)
                json_output['id'] = result['id']
            elif (state == 'absent'):
                result = inventory.delete(name=name, organization=org['id'])
        except exc.NotFound as excinfo:
            module.fail_json(msg='Failed to update inventory, organization not found: {0}'.format(excinfo), changed=False)
        except (exc.ConnectionError, exc.BadRequest) as excinfo:
            module.fail_json(msg='Failed to update inventory: {0}'.format(excinfo), changed=False)
    json_output['changed'] = result['changed']
    module.exit_json(**json_output)