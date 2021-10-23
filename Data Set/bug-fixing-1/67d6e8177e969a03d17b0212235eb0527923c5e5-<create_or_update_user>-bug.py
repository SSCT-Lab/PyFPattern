

def create_or_update_user(connection, module):
    params = dict()
    params['UserName'] = module.params.get('name')
    managed_policies = module.params.get('managed_policy')
    purge_policy = module.params.get('purge_policy')
    changed = False
    if managed_policies:
        managed_policies = convert_friendly_names_to_arns(connection, module, managed_policies)
    user = get_user(connection, module, params['UserName'])
    if (user is None):
        if module.check_mode:
            module.exit_json(changed=True)
        try:
            user = connection.create_user(**params)
            changed = True
        except ClientError as e:
            module.fail_json(msg='Unable to create user: {0}'.format(to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except ParamValidationError as e:
            module.fail_json(msg='Unable to create user: {0}'.format(to_native(e)), exception=traceback.format_exc())
    current_attached_policies = get_attached_policy_list(connection, module, params['UserName'])
    if (not compare_attached_policies(current_attached_policies, managed_policies)):
        current_attached_policies_arn_list = []
        for policy in current_attached_policies:
            current_attached_policies_arn_list.append(policy['PolicyArn'])
        if purge_policy:
            for policy_arn in list((set(current_attached_policies_arn_list) - set(managed_policies))):
                changed = True
                if (not module.check_mode):
                    try:
                        connection.detach_user_policy(UserName=params['UserName'], PolicyArn=policy_arn)
                    except ClientError as e:
                        module.fail_json(msg='Unable to detach policy {0} from user {1}: {2}'.format(policy_arn, params['UserName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                    except ParamValidationError as e:
                        module.fail_json(msg='Unable to detach policy {0} from user {1}: {2}'.format(policy_arn, params['UserName'], to_native(e)), exception=traceback.format_exc())
        if set(managed_policies).difference(set(current_attached_policies_arn_list)):
            changed = True
            if ((managed_policies != [None]) and (not module.check_mode)):
                for policy_arn in managed_policies:
                    try:
                        connection.attach_user_policy(UserName=params['UserName'], PolicyArn=policy_arn)
                    except ClientError as e:
                        module.fail_json(msg='Unable to attach policy {0} to user {1}: {2}'.format(policy_arn, params['UserName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                    except ParamValidationError as e:
                        module.fail_json(msg='Unable to attach policy {0} to user {1}: {2}'.format(policy_arn, params['UserName'], to_native(e)), exception=traceback.format_exc())
    if module.check_mode:
        module.exit_json(changed=changed)
    user = get_user(connection, module, params['UserName'])
    module.exit_json(changed=changed, iam_user=camel_dict_to_snake_dict(user))
