

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(app_name=dict(aliases=['name'], type='str', required=False), description=dict(), state=dict(choices=['present', 'absent'], default='present'), terminate_by_force=dict(type='bool', default=False, required=False)))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    app_name = module.params['app_name']
    description = module.params['description']
    state = module.params['state']
    terminate_by_force = module.params['terminate_by_force']
    if (app_name is None):
        module.fail_json(msg='Module parameter "app_name" is required')
    result = {
        
    }
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    ebs = boto3_conn(module, conn_type='client', resource='elasticbeanstalk', region=region, endpoint=ec2_url, **aws_connect_params)
    app = describe_app(ebs, app_name, module)
    if module.check_mode:
        check_app(ebs, app, module)
        module.fail_json(msg='ASSERTION FAILURE: check_app() should not return control.')
    if (state == 'present'):
        if (app is None):
            try:
                create_app = ebs.create_application(**filter_empty(ApplicationName=app_name, Description=description))
            except (BotoCoreError, ClientError) as e:
                module.fail_json_aws(e, msg='Could not create application')
            app = describe_app(ebs, app_name, module)
            result = dict(changed=True, app=app)
        elif (app.get('Description', None) != description):
            try:
                if (not description):
                    ebs.update_application(ApplicationName=app_name)
                else:
                    ebs.update_application(ApplicationName=app_name, Description=description)
            except (BotoCoreError, ClientError) as e:
                module.fail_json_aws(e, msg='Could not update application')
            app = describe_app(ebs, app_name, module)
            result = dict(changed=True, app=app)
        else:
            result = dict(changed=False, app=app)
    elif (app is None):
        result = dict(changed=False, output='Application not found', app={
            
        })
    else:
        try:
            if terminate_by_force:
                ebs.delete_application(ApplicationName=app_name, TerminateEnvByForce=terminate_by_force)
            else:
                ebs.delete_application(ApplicationName=app_name)
        except (BotoCoreError, ClientError) as e:
            module.fail_json_aws(e, msg='Cannot terminate app')
        result = dict(changed=True, app=app)
    module.exit_json(**result)
