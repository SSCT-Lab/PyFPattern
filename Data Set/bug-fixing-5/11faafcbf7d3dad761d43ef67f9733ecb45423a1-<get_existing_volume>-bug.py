def get_existing_volume(self):
    try:
        volumes = self.client.volumes()
    except APIError as e:
        self.client.fail(text_type(e))
    for volume in volumes['Volumes']:
        if (volume['Name'] == self.parameters.volume_name):
            return volume
    return None