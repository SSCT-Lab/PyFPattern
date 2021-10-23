def delete_snapshot(self):
    '\n        Deletes an existing snapshot\n        '
    snapshot_obj = netapp_utils.zapi.NaElement('snapshot-delete')
    snapshot_obj.add_new_child('snapshot', self.parameters['snapshot'])
    snapshot_obj.add_new_child('volume', self.parameters['volume'])
    if self.parameters.get('ignore_owners'):
        snapshot_obj.add_new_child('ignore-owners', self.parameters['ignore_owners'])
    if self.parameters.get('snapshot_instance_uuid'):
        snapshot_obj.add_new_child('snapshot-instance-uuid', self.parameters['snapshot_instance_uuid'])
    try:
        self.server.invoke_successfully(snapshot_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error deleting snapshot %s: %s' % (self.parameters['snapshot'], to_native(error))), exception=traceback.format_exc())