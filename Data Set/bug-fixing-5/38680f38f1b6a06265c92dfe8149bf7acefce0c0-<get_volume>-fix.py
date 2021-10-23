def get_volume(self, vol_name=None):
    '\n        Return details about the volume\n        :param:\n            name : Name of the volume\n\n        :return: Details about the volume. None if not found.\n        :rtype: dict\n        '
    if (vol_name is None):
        vol_name = self.parameters['name']
    volume_get_iter = self.volume_get_iter(vol_name)
    return_value = None
    if (volume_get_iter.get_child_by_name('num-records') and (int(volume_get_iter.get_child_content('num-records')) > 0)):
        volume_attributes = volume_get_iter.get_child_by_name('attributes-list').get_child_by_name('volume-attributes')
        volume_space_attributes = volume_attributes.get_child_by_name('volume-space-attributes')
        current_size = int(volume_space_attributes.get_child_content('size'))
        volume_state_attributes = volume_attributes.get_child_by_name('volume-state-attributes')
        current_state = volume_state_attributes.get_child_content('state')
        volume_id_attributes = volume_attributes.get_child_by_name('volume-id-attributes')
        aggregate_name = volume_id_attributes.get_child_content('containing-aggregate-name')
        volume_export_attributes = volume_attributes.get_child_by_name('volume-export-attributes')
        policy = volume_export_attributes.get_child_content('policy')
        space_guarantee = volume_space_attributes.get_child_content('space-guarantee')
        is_online = (current_state == 'online')
        return_value = {
            'name': vol_name,
            'size': current_size,
            'is_online': is_online,
            'aggregate_name': aggregate_name,
            'policy': policy,
            'space_guarantee': space_guarantee,
        }
    return return_value