def create_block_device_meta(module, volume):
    MAX_IOPS_TO_SIZE_RATIO = 30
    if ('device_type' in volume):
        if ('volume_type' in volume):
            module.fail_json(msg='device_type is a deprecated name for volume_type. Do not use both device_type and volume_type')
        else:
            module.deprecate('device_type is deprecated for block devices - use volume_type instead', version=2.9)
    if ('device_type' in volume):
        volume['volume_type'] = volume.pop('device_type')
    if (('snapshot' not in volume) and ('ephemeral' not in volume)):
        if ('volume_size' not in volume):
            module.fail_json(msg='Size must be specified when creating a new volume or modifying the root volume')
    if ('snapshot' in volume):
        if ((volume.get('volume_type') == 'io1') and ('iops' not in volume)):
            module.fail_json(msg='io1 volumes must have an iops value set')
    if ('ephemeral' in volume):
        if ('snapshot' in volume):
            module.fail_json(msg='Cannot set both ephemeral and snapshot')
    return_object = {
        
    }
    if ('ephemeral' in volume):
        return_object['VirtualName'] = volume.get('ephemeral')
    if ('device_name' in volume):
        return_object['DeviceName'] = volume.get('device_name')
    if ('no_device' is volume):
        return_object['NoDevice'] = volume.get('no_device')
    if any(((key in volume) for key in ['snapshot', 'volume_size', 'volume_type', 'delete_on_termination', 'ips', 'encrypted'])):
        return_object['Ebs'] = {
            
        }
    if ('snapshot' in volume):
        return_object['Ebs']['SnapshotId'] = volume.get('snapshot')
    if ('volume_size' in volume):
        return_object['Ebs']['VolumeSize'] = int(volume.get('volume_size', 0))
    if ('volume_type' in volume):
        return_object['Ebs']['VolumeType'] = volume.get('volume_type')
    if ('delete_on_termination' in volume):
        return_object['Ebs']['DeleteOnTermination'] = volume.get('delete_on_termination', False)
    if ('iops' in volume):
        return_object['Ebs']['Iops'] = volume.get('iops')
    if ('encrypted' in volume):
        return_object['Ebs']['Encrypted'] = volume.get('encrypted')
    return return_object