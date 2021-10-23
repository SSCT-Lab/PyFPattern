def get_volume(self):
    '\n        Return details about the volume\n        :param:\n            name : Name of the volume\n\n        :return: Details about the volume. None if not found.\n        :rtype: dict\n        '
    volume_info = netapp_utils.zapi.NaElement('volume-get-iter')
    volume_attributes = netapp_utils.zapi.NaElement('volume-attributes')
    volume_id_attributes = netapp_utils.zapi.NaElement('volume-id-attributes')
    volume_id_attributes.add_new_child('name', self.name)
    volume_attributes.add_child_elem(volume_id_attributes)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(volume_attributes)
    volume_info.add_child_elem(query)
    result = self.server.invoke_successfully(volume_info, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        volume_attributes = result.get_child_by_name('attributes-list').get_child_by_name('volume-attributes')
        volume_space_attributes = volume_attributes.get_child_by_name('volume-space-attributes')
        current_size = volume_space_attributes.get_child_content('size')
        volume_state_attributes = volume_attributes.get_child_by_name('volume-state-attributes')
        current_state = volume_state_attributes.get_child_content('state')
        volume_id_attributes = volume_attributes.get_child_by_name('volume-id-attributes')
        aggregate_name = volume_id_attributes.get_child_content('containing-aggregate-name')
        junction_path = volume_id_attributes.get_child_content('junction-path')
        volume_type = volume_id_attributes.get_child_content('type')
        volume_export_attributes = volume_attributes.get_child_by_name('volume-export-attributes')
        policy = volume_export_attributes.get_child_content('policy')
        space_guarantee = volume_space_attributes.get_child_content('space-guarantee')
        percent_snapshot_space = volume_space_attributes.get_child_by_name('percentage-snapshot-reserve')
        is_online = None
        if (current_state == 'online'):
            is_online = True
        elif (current_state == 'offline'):
            is_online = False
        return_value = {
            'name': self.name,
            'size': current_size,
            'is_online': is_online,
            'aggregate_name': aggregate_name,
            'policy': policy,
            'space_guarantee': space_guarantee,
            'percent_snapshot_space': percent_snapshot_space,
            'type': volume_type,
            'junction_path': junction_path,
        }
    return return_value