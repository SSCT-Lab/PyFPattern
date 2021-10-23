def get_attached_policy_list(connection, module, name):
    try:
        return connection.list_attached_user_policies(UserName=name)['AttachedPolicies']
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchEntity'):
            return None
        else:
            module.fail_json(msg='Unable to get policies for user {0}: {1}'.format(name, to_native(e)), **camel_dict_to_snake_dict(e.response))