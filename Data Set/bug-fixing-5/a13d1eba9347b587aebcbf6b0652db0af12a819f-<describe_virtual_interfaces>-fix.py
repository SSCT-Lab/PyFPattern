def describe_virtual_interfaces(client, lag_id):
    try:
        response = client.describe_virtual_interfaces(connectionId=lag_id)
    except botocore.exceptions.ClientError as e:
        raise DirectConnectError(msg='Failed to describe any virtual interfaces associated with LAG: {0}'.format(lag_id), last_traceback=traceback.format_exc(), exception=e)
    return response.get('virtualInterfaces', [])