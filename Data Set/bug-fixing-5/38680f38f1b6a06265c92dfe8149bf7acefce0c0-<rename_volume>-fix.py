def rename_volume(self):
    "\n        Rename the volume.\n\n        Note: 'is_infinite' needs to be set to True in order to rename an\n        Infinite Volume.\n        "
    (vol_rename_zapi, vol_name_zapi) = (['volume-rename-async', 'volume-name'] if self.parameters['is_infinite'] else ['volume-rename', 'volume'])
    volume_rename = netapp_utils.zapi.NaElement.create_node_with_children(vol_rename_zapi, **{
        vol_name_zapi: self.parameters['from_name'],
        'new-volume-name': str(self.parameters['name']),
    })
    try:
        self.server.invoke_successfully(volume_rename, enable_tunneling=True)
        self.ems_log_event('volume-rename')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error renaming volume %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())