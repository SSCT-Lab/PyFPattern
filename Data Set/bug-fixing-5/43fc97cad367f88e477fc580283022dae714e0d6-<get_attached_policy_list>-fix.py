def get_attached_policy_list(connection, module, name):
    try:
        return connection.list_attached_role_policies(RoleName=name)['AttachedPolicies']
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchEntity'):
            return None
        else:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))