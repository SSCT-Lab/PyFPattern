@AWSRetry.backoff(**retry_params)
def create_connection(client, location, bandwidth, name, lag_id):
    if (not name):
        raise DirectConnectError(msg='Failed to create a Direct Connect connection: name required.')
    try:
        if lag_id:
            connection = client.create_connection(location=location, bandwidth=bandwidth, connectionName=name, lagId=lag_id)
        else:
            connection = client.create_connection(location=location, bandwidth=bandwidth, connectionName=name)
    except botocore.exceptions.ClientError as e:
        raise DirectConnectError(msg='Failed to create DirectConnect connection {0}'.format(name), last_traceback=traceback.format_exc(), exception=e)
    return connection['connectionId']