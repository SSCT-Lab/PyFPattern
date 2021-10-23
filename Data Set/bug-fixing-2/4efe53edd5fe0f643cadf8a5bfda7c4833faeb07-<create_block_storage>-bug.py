

def create_block_storage(self):
    volume_name = self.get_key_or_fail('volume_name')
    snapshot_id = self.module.params['snapshot_id']
    if snapshot_id:
        self.module.params['block_size'] = None
        self.module.params['region'] = None
        block_size = None
        region = None
    else:
        block_size = self.get_key_or_fail('block_size')
        region = self.get_key_or_fail('region')
    description = self.module.params['description']
    data = {
        'size_gigabytes': block_size,
        'name': volume_name,
        'description': description,
        'region': region,
        'snapshot_id': snapshot_id,
    }
    response = self.rest.post('volumes', data=data)
    status = response.status_code
    json = response.json
    if (status == 201):
        self.module.exit_json(changed=True, id=json['volume']['id'])
    elif ((status == 409) and (json['id'] == 'already_exists')):
        self.module.exit_json(changed=False)
    else:
        raise DOBlockStorageException(json['message'])
