def create_block_device(module, ec2, volume):
    MAX_IOPS_TO_SIZE_RATIO = 30
    if all(((key in volume) for key in ['device_type', 'volume_type'])):
        module.fail_json(msg='device_type is a deprecated name for volume_type. Do not use both device_type and volume_type')
    volume_type = (volume.get('device_type') or volume.get('volume_type'))
    if (('snapshot' not in volume) and ('ephemeral' not in volume)):
        if ('volume_size' not in volume):
            module.fail_json(msg='Size must be specified when creating a new volume or modifying the root volume')
    if ('snapshot' in volume):
        if ((volume_type == 'io1') and ('iops' not in volume)):
            module.fail_json(msg='io1 volumes must have an iops value set')
        if ('iops' in volume):
            snapshot = ec2.get_all_snapshots(snapshot_ids=[volume['snapshot']])[0]
            size = volume.get('volume_size', snapshot.volume_size)
            if (int(volume['iops']) > (MAX_IOPS_TO_SIZE_RATIO * size)):
                module.fail_json(msg=('IOPS must be at most %d times greater than size' % MAX_IOPS_TO_SIZE_RATIO))
        if ('encrypted' in volume):
            module.fail_json(msg='You can not set encryption when creating a volume from a snapshot')
    if ('ephemeral' in volume):
        if ('snapshot' in volume):
            module.fail_json(msg='Cannot set both ephemeral and snapshot')
    if boto_supports_volume_encryption():
        return BlockDeviceType(snapshot_id=volume.get('snapshot'), ephemeral_name=volume.get('ephemeral'), size=volume.get('volume_size'), volume_type=volume_type, delete_on_termination=volume.get('delete_on_termination', False), iops=volume.get('iops'), encrypted=volume.get('encrypted', None))
    else:
        return BlockDeviceType(snapshot_id=volume.get('snapshot'), ephemeral_name=volume.get('ephemeral'), size=volume.get('volume_size'), volume_type=volume_type, delete_on_termination=volume.get('delete_on_termination', False), iops=volume.get('iops'))