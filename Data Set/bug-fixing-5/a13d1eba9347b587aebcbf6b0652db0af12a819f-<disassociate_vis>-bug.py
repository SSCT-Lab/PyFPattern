def disassociate_vis(client, lag_id, virtual_interfaces):
    for vi in virtual_interfaces:
        delete_virtual_interface(client, vi['virtualInterfaceId'])
        try:
            response = client.delete_virtual_interface(virtualInterfaceId=vi['virtualInterfaceId'])
        except botocore.exceptions.ClientError as e:
            raise DirectConnectError(msg='Could not delete virtual interface {0} to delete link aggregation group {1}.'.format(vi, lag_id), last_traceback=traceback.format_exc(), exception=e)