

def get_volume_info(volume, region):
    attachment = volume['attachments']
    volume_info = {
        'create_time': volume['create_time'],
        'id': volume['volume_id'],
        'encrypted': volume['encrypted'],
        'iops': (volume['iops'] if ('iops' in volume) else None),
        'size': volume['size'],
        'snapshot_id': volume['snapshot_id'],
        'status': volume['state'],
        'type': volume['volume_type'],
        'zone': volume['availability_zone'],
        'region': region,
        'attachment_set': {
            'attach_time': (attachment[0]['attach_time'] if (len(attachment) > 0) else None),
            'device': (attachment[0]['device'] if (len(attachment) > 0) else None),
            'instance_id': (attachment[0]['instance_id'] if (len(attachment) > 0) else None),
            'status': (attachment[0]['state'] if (len(attachment) > 0) else None),
            'delete_on_termination': (attachment[0]['delete_on_termination'] if (len(attachment) > 0) else None),
        },
        'tags': boto3_tag_list_to_ansible_dict(volume['tags']),
    }
    return volume_info
