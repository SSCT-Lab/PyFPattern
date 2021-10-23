

def main():
    module = AnsibleAWSModule(argument_spec={
        'name': dict(type='str', required=True),
        'state': dict(type='str', choices=['present', 'absent'], default='present'),
        'role_arn': dict(type='str'),
        'recording_group': dict(type='dict'),
    }, supports_check_mode=False, required_if=[('state', 'present', ['role_arn', 'recording_group'])])
    result = {
        'changed': False,
    }
    name = module.params.get('name')
    state = module.params.get('state')
    params = {
        
    }
    if name:
        params['name'] = name
    if module.params.get('role_arn'):
        params['roleARN'] = module.params.get('role_arn')
    if module.params.get('recording_group'):
        params['recordingGroup'] = {
            
        }
        if (module.params.get('recording_group').get('all_supported') is not None):
            params['recordingGroup'].update({
                'allSupported': module.params.get('recording_group').get('all_supported'),
            })
        if (module.params.get('recording_group').get('include_global_types') is not None):
            params['recordingGroup'].update({
                'includeGlobalResourceTypes': module.params.get('recording_group').get('include_global_types'),
            })
        if module.params.get('recording_group').get('resource_types'):
            params['recordingGroup'].update({
                'resourceTypes': module.params.get('recording_group').get('resource_types'),
            })
    client = module.client('config', retry_decorator=AWSRetry.jittered_backoff())
    resource_status = resource_exists(client, module, params)
    if (state == 'present'):
        if (not resource_status):
            create_resource(client, module, params, result)
        if resource_status:
            update_resource(client, module, params, result)
    if (state == 'absent'):
        if resource_status:
            delete_resource(client, module, params, result)
    module.exit_json(changed=result['changed'])
