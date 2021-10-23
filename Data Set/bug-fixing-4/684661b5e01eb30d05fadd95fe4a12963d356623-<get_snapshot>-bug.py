def get_snapshot(self, snapshot_name=None):
    "\n        Checks to see if a snapshot exists or not\n        :return: Return True if a snapshot exists, False if it doesn't\n        "
    if (snapshot_name is None):
        snapshot_name = self.parameters['snapshot']
    snapshot_obj = netapp_utils.zapi.NaElement('snapshot-get-iter')
    desired_attr = netapp_utils.zapi.NaElement('desired-attributes')
    snapshot_info = netapp_utils.zapi.NaElement('snapshot-info')
    comment = netapp_utils.zapi.NaElement('comment')
    snapmirror_label = netapp_utils.zapi.NaElement('snapmirror-label')
    snapshot_info.add_child_elem(comment)
    snapshot_info.add_child_elem(snapmirror_label)
    desired_attr.add_child_elem(snapshot_info)
    snapshot_obj.add_child_elem(desired_attr)
    query = netapp_utils.zapi.NaElement('query')
    snapshot_info_obj = netapp_utils.zapi.NaElement('snapshot-info')
    snapshot_info_obj.add_new_child('name', snapshot_name)
    snapshot_info_obj.add_new_child('volume', self.parameters['volume'])
    query.add_child_elem(snapshot_info_obj)
    snapshot_obj.add_child_elem(query)
    result = self.server.invoke_successfully(snapshot_obj, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) == 1)):
        attributes_list = result.get_child_by_name('attributes-list')
        snap_info = attributes_list.get_child_by_name('snapshot-info')
        return_value = {
            'comment': snap_info.get_child_content('comment'),
        }
        if snap_info.get_child_by_name('snapmirror-label'):
            return_value['snapmirror_label'] = snap_info.get_child_content('snapmirror-label')
        else:
            return_value['snapmirror_label'] = None
    return return_value