def ensure_present(client, num_connections, lag_id, lag_name, location, bandwidth, connection_id, min_links, wait, wait_timeout):
    exists = lag_exists(client, lag_id, lag_name)
    if ((not exists) and lag_id):
        raise DirectConnectError(msg='The Direct Connect link aggregation group {0} does not exist.'.format(lag_id), last_traceback=None, response='')
    if exists:
        lag_id = exists
        latest_state = lag_status(client, lag_id)
        if lag_changed(latest_state, lag_name, min_links):
            update_lag(client, lag_id, lag_name, min_links, num_connections, wait, wait_timeout)
            return (True, lag_id)
        return (False, lag_id)
    else:
        lag_id = create_lag(client, num_connections, location, bandwidth, lag_name, connection_id)
        update_lag(client, lag_id, lag_name, min_links, num_connections, wait, wait_timeout)
        return (True, lag_id)