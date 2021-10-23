def resize_volume(self):
    "\n        Re-size the volume.\n\n        Note: 'is_infinite' needs to be set to True in order to rename an\n        Infinite Volume.\n        "
    if self.is_infinite:
        volume_resize = netapp_utils.zapi.NaElement.create_node_with_children('volume-size-async', **{
            'volume-name': self.name,
            'new-size': str(self.size),
        })
    else:
        volume_resize = netapp_utils.zapi.NaElement.create_node_with_children('volume-size', **{
            'volume': self.name,
            'new-size': str(self.size),
        })
    try:
        self.server.invoke_successfully(volume_resize, enable_tunneling=True)
        self.ems_log_event('resize')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error re-sizing volume %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())