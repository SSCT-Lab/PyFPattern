def create_or_update_group(connection, module):
    params = dict()
    params['GroupName'] = module.params.get('name')
    managed_policies = module.params.get('managed_policy')
    if managed_policies:
        managed_policies = convert_friendly_names_to_arns(connection, module, managed_policies)
    users = module.params.get('users')
    purge_users = module.params.get('purge_users')
    purge_policy = module.params.get('purge_policy')
    changed = False
    try:
        group = get_group(connection, module, params['GroupName'])
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    if (group is None):
        try:
            group = connection.create_group(**params)
            changed = True
        except ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except ParamValidationError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc())
    current_attached_policies = get_attached_policy_list(connection, module, params['GroupName'])
    if (not compare_attached_group_policies(current_attached_policies, managed_policies)):
        if purge_policy:
            current_attached_policies_arn_list = []
            for policy in current_attached_policies:
                current_attached_policies_arn_list.append(policy['PolicyArn'])
            for policy_arn in list((set(current_attached_policies_arn_list) - set(managed_policies))):
                try:
                    connection.detach_group_policy(GroupName=params['GroupName'], PolicyArn=policy_arn)
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                except ParamValidationError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc())
        if (managed_policies != [None]):
            for policy_arn in managed_policies:
                try:
                    connection.attach_group_policy(GroupName=params['GroupName'], PolicyArn=policy_arn)
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                except ParamValidationError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc())
        changed = True
    try:
        current_group_members = get_group(connection, module, params['GroupName'])['Users']
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    current_group_members_list = []
    for member in current_group_members:
        current_group_members_list.append(member['UserName'])
    if (not compare_group_members(current_group_members_list, users)):
        if purge_users:
            for user in list((set(current_group_members_list) - set(users))):
                try:
                    connection.remove_user_from_group(GroupName=params['GroupName'], UserName=user)
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                except ParamValidationError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc())
        if (users != [None]):
            for user in users:
                try:
                    connection.add_user_to_group(GroupName=params['GroupName'], UserName=user)
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                except ParamValidationError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc())
        changed = True
    try:
        group = get_group(connection, module, params['GroupName'])
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    module.exit_json(changed=changed, iam_group=camel_dict_to_snake_dict(group))