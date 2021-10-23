def get_role(connection, name, module):
    params = dict()
    params['RoleName'] = name
    try:
        return connection.get_role(**params)['Role']
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchEntity'):
            return None
        else:
            module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))