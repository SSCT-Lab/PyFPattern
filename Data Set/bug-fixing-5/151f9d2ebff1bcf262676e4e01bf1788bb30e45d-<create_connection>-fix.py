def create_connection(client, location, bandwidth, name, lag_id):
    if (not name):
        raise DirectConnectError(msg='Failed to create a Direct Connect connection: name required.')
    params = {
        'location': location,
        'bandwidth': bandwidth,
        'connectionName': name,
    }
    if lag_id:
        params['lagId'] = lag_id
    try:
        connection = AWSRetry.backoff(**retry_params)(client.create_connection)(**params)
    except (BotoCoreError, ClientError) as e:
        raise DirectConnectError(msg='Failed to create DirectConnect connection {0}'.format(name), last_traceback=traceback.format_exc(), exception=e)
    return connection['connectionId']