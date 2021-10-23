def copy_snapshot(module, ec2):
    '\n    Copies an EC2 Snapshot to another region\n\n    module : AnsibleModule object\n    ec2: ec2 connection object\n    '
    params = {
        'SourceRegion': module.params.get('source_region'),
        'SourceSnapshotId': module.params.get('source_snapshot_id'),
        'Description': module.params.get('description'),
    }
    if module.params.get('encrypted'):
        params['Encrypted'] = True
    if module.params.get('kms_key_id'):
        params['KmsKeyId'] = module.params.get('kms_key_id')
    try:
        snapshot_id = ec2.copy_snapshot(**params)['SnapshotId']
        if module.params.get('wait'):
            ec2.get_waiter('snapshot_completed').wait(SnapshotIds=[snapshot_id])
        if module.params.get('tags'):
            ec2.create_tags(Resources=[snapshot_id], Tags=[{
                'Key': k,
                'Value': v,
            } for (k, v) in module.params.get('tags').items()])
    except WaiterError as we:
        module.fail_json(msg=('An error occurred waiting for the snapshot to become available. (%s)' % str(we)), exception=traceback.format_exc())
    except ClientError as ce:
        module.fail_json(msg=str(ce), exception=traceback.format_exc(), **camel_dict_to_snake_dict(ce.response))
    module.exit_json(changed=True, snapshot_id=snapshot_id)