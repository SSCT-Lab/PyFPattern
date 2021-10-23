def create_snapshot(self):
    '\n        Creates a new snapshot\n        '
    snapshot_obj = netapp_utils.zapi.NaElement('snapshot-create')
    snapshot_obj.add_new_child('snapshot', self.parameters['snapshot'])
    snapshot_obj.add_new_child('volume', self.parameters['volume'])
    if self.parameters.get('async_bool'):
        snapshot_obj.add_new_child('async', self.parameters['async_bool'])
    if self.parameters.get('comment'):
        snapshot_obj.add_new_child('comment', self.parameters['comment'])
    if self.parameters.get('snapmirror_label'):
        snapshot_obj.add_new_child('snapmirror-label', self.parameters['snapmirror_label'])
    try:
        self.server.invoke_successfully(snapshot_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error creating snapshot %s: %s' % (self.parameters['snapshot'], to_native(error))), exception=traceback.format_exc())