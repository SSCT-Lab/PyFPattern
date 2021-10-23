def list_ec2_snapshots(connection, module):
    snapshot_ids = module.params.get('snapshot_ids')
    owner_ids = [str(owner_id) for owner_id in module.params.get('owner_ids')]
    restorable_by_user_ids = [str(user_id) for user_id in module.params.get('restorable_by_user_ids')]
    filters = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    try:
        snapshots = connection.describe_snapshots(SnapshotIds=snapshot_ids, OwnerIds=owner_ids, RestorableByUserIds=restorable_by_user_ids, Filters=filters)
    except ClientError as e:
        module.fail_json(msg=e.message)
    snaked_snapshots = []
    for snapshot in snapshots['Snapshots']:
        snaked_snapshots.append(camel_dict_to_snake_dict(snapshot))
    for snapshot in snaked_snapshots:
        if ('tags' in snapshot):
            snapshot['tags'] = boto3_tag_list_to_ansible_dict(snapshot['tags'], 'key', 'value')
    module.exit_json(snapshots=snaked_snapshots)