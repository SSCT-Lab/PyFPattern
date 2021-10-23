

def main():
    argument_spec = dict(name=dict(Required=True), value=dict(Required=True))
    module = TowerModule(argument_spec=argument_spec, supports_check_mode=False)
    json_output = {
        
    }
    name = module.params.get('name')
    value = module.params.get('value')
    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        try:
            setting = tower_cli.get_resource('setting')
            result = setting.modify(setting=name, value=value)
            json_output['id'] = result['id']
            json_output['value'] = result['value']
        except (exc.ConnectionError, exc.BadRequest, exc.AuthError) as excinfo:
            module.fail_json(msg='Failed to modify the setting: {0}'.format(excinfo), changed=False)
    json_output['changed'] = result['changed']
    module.exit_json(**json_output)
