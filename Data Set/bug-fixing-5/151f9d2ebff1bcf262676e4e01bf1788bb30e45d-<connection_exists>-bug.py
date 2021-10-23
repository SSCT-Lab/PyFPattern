@AWSRetry.backoff(**retry_params)
def connection_exists(client, connection_id=None, connection_name=None, verify=True):
    try:
        if connection_id:
            response = client.describe_connections(connectionId=connection_id)
        else:
            response = client.describe_connections()
    except botocore.exceptions.ClientError as e:
        raise DirectConnectError(msg='Failed to describe DirectConnect ID {0}'.format(connection_id), last_traceback=traceback.format_exc(), exception=e)
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