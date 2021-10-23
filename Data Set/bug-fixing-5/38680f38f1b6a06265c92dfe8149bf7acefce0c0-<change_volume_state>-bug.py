def change_volume_state(self):
    "\n        Change volume's state (offline/online).\n\n        "
    state_requested = None
    if self.is_online:
        state_requested = 'online'
        if self.is_infinite:
            volume_change_state = netapp_utils.zapi.NaElement.create_node_with_children('volume-online-async', **{
                'volume-name': self.name,
            })
        else:
            volume_change_state = netapp_utils.zapi.NaElement.create_node_with_children('volume-online', **{
                'name': self.name,
            })
    else:
        state_requested = 'offline'
        volume_unmount = netapp_utils.zapi.NaElement.create_node_with_children('volume-unmount', **{
            'volume-name': self.name,
        })
        if self.is_infinite:
            volume_change_state = netapp_utils.zapi.NaElement.create_node_with_children('volume-offline-async', **{
                'volume-name': self.name,
            })
        else:
            volume_change_state = netapp_utils.zapi.NaElement.create_node_with_children('volume-offline', **{
                'name': self.name,
            })
    try:
        if (state_requested == 'offline'):
            self.server.invoke_successfully(volume_unmount, enable_tunneling=True)
        self.server.invoke_successfully(volume_change_state, enable_tunneling=True)
        self.ems_log_event('change')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error changing the state of                                   volume %s to %s: %s' % (self.name, state_requested, to_native(error))), exception=traceback.format_exc())