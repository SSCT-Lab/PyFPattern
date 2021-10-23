def connection_exists(client, connection_id=None, connection_name=None, verify=True):
    params = {
        
    }
    if connection_id:
        params['connectionId'] = connection_id
    try:
        response = AWSRetry.backoff(**retry_params)(client.describe_connections)(**params)
    except (BotoCoreError, ClientError) as e:
        if connection_id:
            msg = 'Failed to describe DirectConnect ID {0}'.format(connection_id)
        else:
            msg = 'Failed to describe DirectConnect connections'
        raise DirectConnectError(msg=msg, last_traceback=traceback.format_exc(), exception=e)
    match = []
    connection = []
    if ((len(response.get('connections', [])) == 1) and connection_id):
        if (response['connections'][0]['connectionState'] != 'deleted'):
            match.append(response['connections'][0]['connectionId'])
            connection.extend(response['connections'])
    for conn in response.get('connections', []):
        if ((connection_name == conn['connectionName']) and (conn['connectionState'] != 'deleted')):
            match.append(conn['connectionId'])
            connection.append(conn)
    if (verify and (len(match) == 1)):
        return match[0]
    elif verify:
        return False
    elif (len(connection) == 1):
        return {
            'connection': connection[0],
        }
    return {
        'connection': {
            
        },
    }