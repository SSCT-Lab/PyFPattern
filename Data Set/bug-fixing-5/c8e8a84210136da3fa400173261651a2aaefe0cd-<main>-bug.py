def main():
    argument_spec = dict(name=dict(required=True), description=dict(required=False), inventory=dict(required=True), source=dict(required=True, choices=SOURCE_CHOICES.keys()), credential=dict(required=False), source_vars=dict(required=False), timeout=dict(type='int', required=False), source_project=dict(required=False), source_path=dict(required=False), update_on_project_update=dict(type='bool', required=False), source_regions=dict(required=False), instance_filters=dict(required=False), group_by=dict(required=False), source_script=dict(required=False), overwrite=dict(type='bool', required=False), overwrite_vars=dict(type='bool', required=False), update_on_launch=dict(type='bool', required=False), update_cache_timeout=dict(type='int', required=False), state=dict(choices=['present', 'absent'], default='present'))
    module = TowerModule(argument_spec=argument_spec, supports_check_mode=True)
    name = module.params.get('name')
    inventory = module.params.get('inventory')
    source = module.params.get('source')
    state = module.params.get('state')
    json_output = {
        'inventory_source': name,
        'state': state,
    }
    tower_auth = tower_auth_config(module)
    with settings.runtime_values(**tower_auth):
        tower_check_mode(module)
        inventory_source = tower_cli.get_resource('inventory_source')
        try:
            params = {
                
            }
            params['name'] = name
            params['source'] = source
            if module.params.get('description'):
                params['description'] = module.params.get('description')
            if module.params.get('credential'):
                credential_res = tower_cli.get_resource('credential')
                try:
                    credential = credential_res.get(name=module.params.get('credential'))
                    params['credential'] = credential['id']
                except exc.NotFound as excinfo:
                    module.fail_json(msg='Failed to update credential source,credential not found: {0}'.format(excinfo), changed=False)
            if module.params.get('source_project'):
                source_project_res = tower_cli.get_resource('project')
                try:
                    source_project = source_project_res.get(name=module.params.get('source_project'))
                    params['source_project'] = source_project['id']
                except exc.NotFound as excinfo:
                    module.fail_json(msg='Failed to update source project,project not found: {0}'.format(excinfo), changed=False)
            if module.params.get('source_script'):
                source_script_res = tower_cli.get_resource('inventory_script')
                try:
                    script = source_script_res.get(name=module.params.get('source_script'))
                    params['source_script'] = script['id']
                except exc.NotFound as excinfo:
                    module.fail_json(msg='Failed to update source script,script not found: {0}'.format(excinfo), changed=False)
            try:
                inventory_res = tower_cli.get_resource('inventory')
                params['inventory'] = inventory_res.get(name=inventory)['id']
            except exc.NotFound as excinfo:
                module.fail_json(msg='Failed to update inventory source, inventory not found: {0}'.format(excinfo), changed=False)
            for key in ('source_vars', 'timeout', 'source_path', 'update_on_project_update', 'source_regions', 'instance_filters', 'group_by', 'overwrite', 'overwrite_vars', 'update_on_launch', 'update_cache_timeout'):
                if module.params.get(key):
                    params[key] = module.params.get(key)
            if (state == 'present'):
                params['create_on_missing'] = True
                result = inventory_source.modify(**params)
                json_output['id'] = result['id']
            elif (state == 'absent'):
                params['fail_on_missing'] = False
                result = inventory_source.delete(**params)
        except (exc.ConnectionError, exc.BadRequest) as excinfo:
            module.fail_json(msg='Failed to update inventory source:                     {0}'.format(excinfo), changed=False)
    json_output['changed'] = result['changed']
    module.exit_json(**json_output)