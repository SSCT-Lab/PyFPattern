def update_lag(client, lag_id, lag_name, min_links, num_connections, wait, wait_timeout):
    start = time.time()
    if (min_links and (min_links > num_connections)):
        raise DirectConnectError(msg='The number of connections {0} must be greater than the minimum number of links {1} to update the LAG {2}'.format(num_connections, min_links, lag_id), last_traceback=None, exception=None)
    while True:
        try:
            _update_lag(client, lag_id, lag_name, min_links)
        except botocore.exceptions.ClientError as e:
            if (wait and ((time.time() - start) <= wait_timeout)):
                continue
            msg = 'Failed to update Direct Connect link aggregation group {0}.'.format(lag_id)
            if ('MinimumLinks cannot be set higher than the number of connections' in e.response['Error']['Message']):
                msg += 'Unable to set the min number of links to {0} while the LAG connections are being requested'.format(min_links)
            raise DirectConnectError(msg=msg, last_traceback=traceback.format_exc(), exception=e)
        else:
            break