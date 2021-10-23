def ensure_absent(client, lag_id, lag_name, force_delete, delete_with_disassociation, wait, wait_timeout):
    lag_id = lag_exists(client, lag_id, lag_name)
    if (not lag_id):
        return False
    latest_status = lag_status(client, lag_id)
    (virtual_interfaces, connections) = get_connections_and_virtual_interfaces(client, lag_id)
    if (any((latest_status['minimumLinks'], virtual_interfaces, connections)) and (not force_delete)):
        raise DirectConnectError(msg='There are a minimum number of links, hosted connections, or associated virtual interfaces for LAG {0}. To force deletion of the LAG use delete_force: True (if the LAG has virtual interfaces they will be deleted). Optionally, to ensure hosted connections are deleted after disassociation use delete_with_disassociation: True and wait: True (as Virtual Interfaces may take a few moments to delete)'.format(lag_id), last_traceback=None, exception=None)
    update_lag(client, lag_id, None, 0, len(connections), wait, wait_timeout)
    for connection in connections:
        disassociate_connection_and_lag(client, connection['connectionId'], lag_id)
        if delete_with_disassociation:
            delete_connection(client, connection['connectionId'])
    for vi in virtual_interfaces:
        delete_virtual_interface(client, vi['virtualInterfaceId'])
    start_time = time.time()
    while True:
        try:
            delete_lag(client, lag_id)
        except DirectConnectError as e:
            if (('until its Virtual Interfaces are deleted' in e.exception) and ((time.time() - start_time) < wait_timeout) and wait):
                continue
        else:
            return True