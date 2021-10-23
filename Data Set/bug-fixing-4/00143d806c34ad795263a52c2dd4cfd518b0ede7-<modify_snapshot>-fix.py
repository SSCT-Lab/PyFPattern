def modify_snapshot(self):
    '\n        Modify an existing snapshot\n        :return:\n        '
    snapshot_obj = netapp_utils.zapi.NaElement('snapshot-modify-iter')
    query = netapp_utils.zapi.NaElement('query')
    snapshot_info_obj = netapp_utils.zapi.NaElement('snapshot-info')
    snapshot_info_obj.add_new_child('name', self.snapshot)
    query.add_child_elem(snapshot_info_obj)
    snapshot_obj.add_child_elem(query)
    attributes = netapp_utils.zapi.NaElement('attributes')
    snapshot_info_obj = netapp_utils.zapi.NaElement('snapshot-info')
    snapshot_info_obj.add_new_child('name', self.snapshot)
    if (self.comment is not None):
        snapshot_info_obj.add_new_child('comment', self.comment)
    attributes.add_child_elem(snapshot_info_obj)
    snapshot_obj.add_child_elem(attributes)
    try:
        self.server.invoke_successfully(snapshot_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error modifying snapshot %s: %s' % (self.snapshot, to_native(error))), exception=traceback.format_exc())