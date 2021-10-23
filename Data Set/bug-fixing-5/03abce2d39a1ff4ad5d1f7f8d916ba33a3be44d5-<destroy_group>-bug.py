def destroy_group(connection, module):
    params = dict()
    params['GroupName'] = module.params.get('name')
    if get_group(connection, module, params['GroupName']):
        try:
            for policy in get_attached_policy_list(connection, module, params['GroupName']):
                connection.detach_group_policy(GroupName=params['GroupName'], PolicyArn=policy['PolicyArn'])
        except ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except ParamValidationError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc())
        current_group_members_list = []
        current_group_members = get_group(connection, module, params['GroupName'])['Users']
        for member in current_group_members:
            current_group_members_list.append(member['UserName'])
        for user in current_group_members_list:
            try:
                connection.remove_user_from_group(GroupName=params['GroupName'], UserName=user)
            except ClientError as e:
                module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
            except ParamValidationError as e:
                module.fail_json(msg=e.message, exception=traceback.format_exc())
        try:
            connection.delete_group(**params)
        except ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except ParamValidationError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc())
    else:
        module.exit_json(changed=False)
    module.exit_json(changed=True)