def destroy_role(connection, module):
    params = dict()
    params['RoleName'] = module.params.get('name')
    if get_role(connection, params['RoleName']):
        try:
            instance_profiles = connection.list_instance_profiles_for_role(RoleName=params['RoleName'])['InstanceProfiles']
        except ClientError as e:
            module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))
        for profile in instance_profiles:
            try:
                connection.remove_role_from_instance_profile(InstanceProfileName=profile['InstanceProfileName'], RoleName=params['RoleName'])
            except ClientError as e:
                module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))
        try:
            for policy in get_attached_policy_list(connection, params['RoleName']):
                connection.detach_role_policy(RoleName=params['RoleName'], PolicyArn=policy['PolicyArn'])
        except (ClientError, ParamValidationError) as e:
            module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))
        try:
            connection.delete_role(**params)
        except ClientError as e:
            module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))
    else:
        module.exit_json(changed=False)
    module.exit_json(changed=True)