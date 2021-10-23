def delete_lag(client, lag_id):
    try:
        client.delete_lag(lagId=lag_id)
    except botocore.exceptions.ClientError as e:
        raise DirectConnectError(msg='Failed to delete Direct Connect link aggregation group {0}.'.format(lag_id), last_traceback=traceback.format_exc(), exception=e)