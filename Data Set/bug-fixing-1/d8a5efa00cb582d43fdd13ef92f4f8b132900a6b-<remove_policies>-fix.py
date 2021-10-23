

def remove_policies(connection, module, policies_to_remove, params):
    changed = False
    for policy in policies_to_remove:
        try:
            if (not module.check_mode):
                connection.detach_role_policy(RoleName=params['RoleName'], PolicyArn=policy)
        except ClientError as e:
            module.fail_json(msg='Unable to detach policy {0} from {1}: {2}'.format(policy, params['RoleName'], to_native(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except BotoCoreError as e:
            module.fail_json(msg='Unable to detach policy {0} from {1}: {2}'.format(policy, params['RoleName'], to_native(e)), exception=traceback.format_exc())
        changed = True
    return changed
