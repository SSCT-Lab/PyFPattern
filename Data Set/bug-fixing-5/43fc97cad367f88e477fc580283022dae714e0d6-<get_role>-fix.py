def get_role(connection, module, name):
    try:
        return connection.get_role(RoleName=name)['Role']
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchEntity'):
            return None
        else:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    except NoCredentialsError as e:
        module.fail_json(msg=('AWS authentication problem. ' + e.message), exception=traceback.format_exc())