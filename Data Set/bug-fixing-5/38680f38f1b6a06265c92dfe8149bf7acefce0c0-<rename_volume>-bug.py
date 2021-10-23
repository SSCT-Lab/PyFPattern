def rename_volume(self):
    "\n        Rename the volume.\n\n        Note: 'is_infinite' needs to be set to True in order to rename an\n        Infinite Volume.\n        "
    if self.is_infinite:
        volume_rename = netapp_utils.zapi.NaElement.create_node_with_children('volume-rename-async', **{
            'volume-name': self.name,
            'new-volume-name': str(self.new_name),
        })
    else:
        volume_rename = netapp_utils.zapi.NaElement.create_node_with_children('volume-rename', **{
            'volume': self.name,
            'new-volume-name': str(self.new_name),
        })
    try:
        self.server.invoke_successfully(volume_rename, enable_tunneling=True)
        self.ems_log_event('rename')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error renaming volume %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())