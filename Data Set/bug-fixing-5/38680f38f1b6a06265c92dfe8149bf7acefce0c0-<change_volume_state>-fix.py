def change_volume_state(self):
    "\n        Change volume's state (offline/online).\n        "
    if self.parameters['is_online']:
        (vol_state_zapi, vol_name_zapi) = (['volume-online-async', 'volume-name'] if self.parameters['is_infinite'] else ['volume-online', 'name'])
    else:
        (vol_state_zapi, vol_name_zapi) = (['volume-offline-async', 'volume-name'] if self.parameters['is_infinite'] else ['volume-offline', 'name'])
        volume_unmount = netapp_utils.zapi.NaElement.create_node_with_children('volume-unmount', **{
            'volume-name': self.parameters['name'],
        })
    volume_change_state = netapp_utils.zapi.NaElement.create_node_with_children(vol_state_zapi, **{
        vol_name_zapi: self.parameters['name'],
    })
    try:
        if (not self.parameters['is_online']):
            self.server.invoke_successfully(volume_unmount, enable_tunneling=True)
        self.server.invoke_successfully(volume_change_state, enable_tunneling=True)
        self.ems_log_event('change-state')
    except netapp_utils.zapi.NaApiError as error:
        state = ('online' if self.parameters['is_online'] else 'offline')
        self.module.fail_json(msg=('Error changing the state of volume %s to %s: %s' % (self.parameters['name'], state, to_native(error))), exception=traceback.format_exc())