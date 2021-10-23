def move_volume(self):
    'Move volume from source aggregate to destination aggregate'
    volume_move = netapp_utils.zapi.NaElement.create_node_with_children('volume-move-start', **{
        'source-volume': self.name,
        'vserver': self.vserver,
        'dest-aggr': self.aggregate_name,
    })
    try:
        self.cluster.invoke_successfully(volume_move, enable_tunneling=True)
        self.ems_log_event('move')
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error moving volume %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())