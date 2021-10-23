def create_or_update_role(connection, module):
    params = dict()
    params['Path'] = module.params.get('path')
    params['RoleName'] = module.params.get('name')
    params['AssumeRolePolicyDocument'] = module.params.get('assume_role_policy_document')
    if (module.params.get('description') is not None):
        params['Description'] = module.params.get('description')
    managed_policies = module.params.get('managed_policy')
    create_instance_profile = module.params.get('create_instance_profile')
    if managed_policies:
        managed_policies = convert_friendly_names_to_arns(connection, module, managed_policies)
    changed = False
    role = get_role(connection, module, params['RoleName'])
    if (role is None):
        try:
            if (not module.check_mode):
                role = connection.create_role(**params)
            else:
                role = {
                    'MadeInCheckMode': True,
                }
                role['AssumeRolePolicyDocument'] = json.loads(params['AssumeRolePolicyDocument'])
            changed = True
        except ClientError as e:
            module.fail_json(msg='Unable to create role: {0}'.format(to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except BotoCoreError as e:
            module.fail_json(msg='Unable to create role: {0}'.format(to_native(e)), exception=traceback.format_exc())
    elif (not compare_assume_role_policy_doc(role['AssumeRolePolicyDocument'], params['AssumeRolePolicyDocument'])):
        try:
            if (not module.check_mode):
                connection.update_assume_role_policy(RoleName=params['RoleName'], PolicyDocument=json.dumps(json.loads(params['AssumeRolePolicyDocument'])))
            changed = True
        except ClientError as e:
            module.fail_json(msg='Unable to update assume role policy for role {0}: {1}'.format(params['RoleName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except BotoCoreError as e:
            module.fail_json(msg='Unable to update assume role policy for role {0}: {1}'.format(params['RoleName'], to_native(e)), exception=traceback.format_exc())
    if (managed_policies is not None):
        current_attached_policies = get_attached_policy_list(connection, module, params['RoleName'])
        current_attached_policies_arn_list = [policy['PolicyArn'] for policy in current_attached_policies]
        if ((len(managed_policies) == 1) and (not managed_policies[0]) and module.params.get('purge_policies')):
            if remove_policies(connection, module, (set(current_attached_policies_arn_list) - set(managed_policies)), params):
                changed = True
        else:
            if module.params.get('purge_policies'):
                if remove_policies(connection, module, (set(current_attached_policies_arn_list) - set(managed_policies)), params):
                    changed = True
            for policy_arn in (set(managed_policies) - set(current_attached_policies_arn_list)):
                try:
                    if (not module.check_mode):
                        connection.attach_role_policy(RoleName=params['RoleName'], PolicyArn=policy_arn)
                except ClientError as e:
                    module.fail_json(msg='Unable to attach policy {0} to role {1}: {2}'.format(policy_arn, params['RoleName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                except BotoCoreError as e:
                    module.fail_json(msg='Unable to attach policy {0} to role {1}: {2}'.format(policy_arn, params['RoleName'], to_native(e)), exception=traceback.format_exc())
                changed = True
    if (create_instance_profile and (not role.get('MadeInCheckMode', False))):
        try:
            instance_profiles = connection.list_instance_profiles_for_role(RoleName=params['RoleName'])['InstanceProfiles']
        except ClientError as e:
            module.fail_json(msg='Unable to list instance profiles for role {0}: {1}'.format(params['RoleName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except BotoCoreError as e:
            module.fail_json(msg='Unable to list instance profiles for role {0}: {1}'.format(params['RoleName'], to_native(e)), exception=traceback.format_exc())
        if (not any(((p['InstanceProfileName'] == params['RoleName']) for p in instance_profiles))):
            try:
                if (not module.check_mode):
                    connection.create_instance_profile(InstanceProfileName=params['RoleName'], Path=params['Path'])
                changed = True
            except ClientError as e:
                if (e.response['Error']['Code'] == 'EntityAlreadyExists'):
                    pass
                else:
                    module.fail_json(msg='Unable to create instance profile for role {0}: {1}'.format(params['RoleName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
            except BotoCoreError as e:
                module.fail_json(msg='Unable to create instance profile for role {0}: {1}'.format(params['RoleName'], to_native(e)), exception=traceback.format_exc())
            if (not module.check_mode):
                connection.add_role_to_instance_profile(InstanceProfileName=params['RoleName'], RoleName=params['RoleName'])
    if (not role.get('MadeInCheckMode', False)):
        role = get_role(connection, module, params['RoleName'])
        role['attached_policies'] = get_attached_policy_list(connection, module, params['RoleName'])
    module.exit_json(changed=changed, iam_role=camel_dict_to_snake_dict(role), **camel_dict_to_snake_dict(role))