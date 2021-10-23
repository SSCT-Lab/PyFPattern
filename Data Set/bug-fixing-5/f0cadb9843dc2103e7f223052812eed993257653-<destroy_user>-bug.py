def destroy_user(connection, module):
    params = dict()
    params['UserName'] = module.params.get('name')
    if get_user(connection, module, params['UserName']):
        if module.check_mode:
            module.exit_json(changed=True)
        try:
            for policy in get_attached_policy_list(connection, module, params['UserName']):
                connection.detach_user_policy(UserName=params['UserName'], PolicyArn=policy['PolicyArn'])
        except ClientError as e:
            module.fail_json(msg='Unable to detach policy {0} from user {1}: {2}'.format(policy['PolicyArn'], params['UserName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except ParamValidationError as e:
            module.fail_json(msg='Unable to detach policy {0} from user {1}: {2}'.format(policy['PolicyArn'], params['UserName'], to_native(e)), exception=traceback.format_exc())
        try:
            connection.delete_user(**params)
        except ClientError as e:
            module.fail_json(msg='Unable to delete user {0}: {1}'.format(params['UserName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except ParamValidationError as e:
            module.fail_json(msg='Unable to delete user {0}: {1}'.format(params['UserName'], to_native(e)), exception=traceback.format_exc())
    else:
        module.exit_json(changed=False)
    module.exit_json(changed=True)