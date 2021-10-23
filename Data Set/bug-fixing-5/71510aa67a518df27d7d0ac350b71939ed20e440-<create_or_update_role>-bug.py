def create_or_update_role(connection, module):
    params = dict()
    params['Path'] = module.params.get('path')
    params['RoleName'] = module.params.get('name')
    params['AssumeRolePolicyDocument'] = module.params.get('assume_role_policy_document')
    if (module.params.get('description') is not None):
        params['Description'] = module.params.get('description')
    managed_policies = module.params.get('managed_policy')
    if managed_policies:
        managed_policies = convert_friendly_names_to_arns(connection, module, managed_policies)
    changed = False
    role = get_role(connection, module, params['RoleName'])
    if (role is None):
        try:
            role = connection.create_role(**params)
            changed = True
        except ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    elif (not compare_assume_role_policy_doc(role['AssumeRolePolicyDocument'], params['AssumeRolePolicyDocument'])):
        try:
            connection.update_assume_role_policy(RoleName=params['RoleName'], PolicyDocument=json.dumps(json.loads(params['AssumeRolePolicyDocument'])))
            changed = True
        except ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    if (managed_policies is not None):
        current_attached_policies = get_attached_policy_list(connection, module, params['RoleName'])
        if ((len(managed_policies) == 1) and (not managed_policies[0])):
            for policy in current_attached_policies:
                try:
                    connection.detach_role_policy(RoleName=params['RoleName'], PolicyArn=policy['PolicyArn'])
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                changed = True
        else:
            current_attached_policies_arn_list = []
            for policy in current_attached_policies:
                current_attached_policies_arn_list.append(policy['PolicyArn'])
            for policy_arn in list((set(current_attached_policies_arn_list) - set(managed_policies))):
                try:
                    connection.detach_role_policy(RoleName=params['RoleName'], PolicyArn=policy_arn)
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                changed = True
            for policy_arn in list((set(managed_policies) - set(current_attached_policies_arn_list))):
                try:
                    connection.attach_role_policy(RoleName=params['RoleName'], PolicyArn=policy_arn)
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                changed = True
    try:
        instance_profiles = connection.list_instance_profiles_for_role(RoleName=params['RoleName'])['InstanceProfiles']
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    if (not any(((p['InstanceProfileName'] == params['RoleName']) for p in instance_profiles))):
        try:
            connection.create_instance_profile(InstanceProfileName=params['RoleName'], Path=params['Path'])
            changed = True
        except ClientError as e:
            if (e.response['Error']['Code'] == 'EntityAlreadyExists'):
                pass
            else:
                module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        connection.add_role_to_instance_profile(InstanceProfileName=params['RoleName'], RoleName=params['RoleName'])
    role = get_role(connection, module, params['RoleName'])
    role['attached_policies'] = get_attached_policy_list(connection, module, params['RoleName'])
    module.exit_json(changed=changed, iam_role=camel_dict_to_snake_dict(role), **camel_dict_to_snake_dict(role))