def get_group(connection, module, name):
    params = dict()
    params['GroupName'] = name
    try:
        return connection.get_group(**params)
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchEntity'):
            return None
        else:
            module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))