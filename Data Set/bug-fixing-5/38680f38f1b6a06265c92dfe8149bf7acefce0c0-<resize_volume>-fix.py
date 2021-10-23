def resize_volume(self):
    "\n        Re-size the volume.\n\n        Note: 'is_infinite' needs to be set to True in order to rename an\n        Infinite Volume.\n        "
    (vol_size_zapi, vol_name_zapi) = (['volume-size-async', 'volume-name'] if self.parameters['is_infinite'] else ['volume-size', 'volume'])
    volume_resize = netapp_utils.zapi.NaElement.create_node_with_children(vol_size_zapi, **{
        vol_name_zapi: self.parameters['name'],
        'new-size': str(self.parameters['size']),
    })
    try:
        self.server.invoke_successfully(volume_resize, enable_tunneling=True)
        self.ems_log_event('volume-resize')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error re-sizing volume %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())