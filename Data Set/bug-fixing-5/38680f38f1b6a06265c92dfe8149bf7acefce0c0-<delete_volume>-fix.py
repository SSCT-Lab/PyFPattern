def delete_volume(self):
    'Delete ONTAP volume'
    if self.parameters.get('is_infinite'):
        volume_delete = netapp_utils.zapi.NaElement.create_node_with_children('volume-destroy-async', **{
            'volume-name': self.parameters['name'],
        })
    else:
        volume_delete = netapp_utils.zapi.NaElement.create_node_with_children('volume-destroy', **{
            'name': self.parameters['name'],
            'unmount-and-offline': 'true',
        })
    try:
        self.server.invoke_successfully(volume_delete, enable_tunneling=True)
        self.ems_log_event('delete')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error deleting volume %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())