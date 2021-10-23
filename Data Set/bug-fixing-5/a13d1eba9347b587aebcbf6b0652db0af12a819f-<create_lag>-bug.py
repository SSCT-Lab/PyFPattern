def create_lag(client, num_connections, location, bandwidth, name, connection_id):
    if (not name):
        raise DirectConnectError(msg='Failed to create a Direct Connect link aggregation group: name required.')
    parameters = dict(numberOfConnections=num_connections, location=location, connectionsBandwidth=bandwidth, lagName=name)
    if connection_id:
        parameters.update(connectionId=connection_id)
    try:
        lag = client.create_lag(**parameters)
    except botocore.exceptions.ClientError as e:
        raise DirectConnectError(msg='Failed to create DirectConnect link aggregation group {0}'.format(name), last_traceback=traceback.format_exc(), exception=e)
    return lag['lagId']